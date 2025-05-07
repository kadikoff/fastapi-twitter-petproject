from pathlib import Path
from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import Result, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from server.api.crud import crud_medias
from server.core.models import Likes, Tweets, Users
from server.core.schemas.schemas_tweets import TweetCreate
from server.utils.media_writer import delete_media


async def create_tweet(
    session: AsyncSession, user: Users, tweet_in: TweetCreate
) -> Tweets:
    """Создание нового твита в таблице Tweets

    В случае, если пользователь выкладывает твит вместе
    с медиа-файлами, они сохраняются в таблице Medias, затем фронтенд
    будет подгружать медиа-файла туда автоматически при отправке твита
    и подставлять id медиа-файлов оттуда в json.

    Используется в эндпоинте:
    - POST /api/tweets - создать твит
    """

    new_tweet = Tweets(tweet_data=tweet_in.tweet_data, user_id=user.id)
    session.add(new_tweet)

    if tweet_in.tweet_media_ids:
        await session.flush()
        await crud_medias.update_media(
            session=session,
            tweet=new_tweet,
            tweet_media_ids=tweet_in.tweet_media_ids,
        )

    await session.commit()
    return new_tweet


async def get_tweets(
    session: AsyncSession,
    current_user: Users,
    offset: int,
    limit: int,
) -> list[Tweets | None]:
    """Получение списка всех твитов из таблицы Tweets

    При запросе пользователь получит ленту твитов
    отсортированных в порядке убывания по популярности
    от пользователей, на которых он подписан

    Используется в эндпоинте:
    - GET /api/tweets - получить информации о всех твитах
    """

    following_ids: list[int] = [user.id for user in current_user.following]
    following_ids.append(current_user.id)

    # Логика пагинации:
    #
    # Если пользователь включил пагинацию на сайте,
    # то есть передал Query-параметры offset и limit:
    # - start - начало диапазона выборки = (номер_стр - 1) * размер_стр
    # - stop - конец диапазона выборки = (номер_стр * размер_стр)
    #
    # Пример для offset=2, limit=10:
    # - start = (2 - 1) * 10 = 10 (получим элементы массива с индекса 10)
    # - stop = 2 * 10 = 20 (по индекс 20)
    #
    # В данном случае start и stop это индексы элементов из массива
    # с выдачей твитов, пример (аналогия): tweets_massive[start:stop]
    if offset != 0:
        start = (offset - 1) * limit
        stop = offset * limit

    # Если пагинация не используется (Query-параметры offset и limit
    # не переданы), то по умолчанию в эту функцию передаются
    # offset=0 и limit=50, то есть из бд получим
    # первые 50 твитов (start=0, stop=50)
    else:
        start = offset
        stop = limit

    stmt = (
        select(Tweets)
        .filter(Tweets.user_id.in_(following_ids))
        .options(
            joinedload(Tweets.user),
            joinedload(Tweets.likes).subqueryload(Likes.user),
            joinedload(Tweets.medias),
        )
        .outerjoin(Tweets.likes)
        .group_by(Tweets)
        .order_by(desc(func.count(Tweets.likes)), Tweets.tweet_id)
        .slice(start, stop)
    )

    db_response: Result = await session.execute(stmt)
    tweets: Sequence[Tweets] = db_response.unique().scalars().all()

    return list(tweets)


async def delete_tweet(
    session: AsyncSession, tweet_id: int, current_user: Users
) -> None:
    """Удаление твита из таблицы Tweets

    Пользователь может удалить только свой твит, то есть тот,
    который он выкладывал со своего аккаунта.

    В случае, если твит уже удалён или его нет - возвращается
    сообщение об ошибке.

    Также, если пользователь пытается удалить чужой твит -
    возвращается сообщение об ошибке.

    Применяется каскадное удаление записей из дочерних таблиц,
    связанных с конкретным твитом. Также удаляются и медиа-файлы
    из директории хранения на сервере.

    Используется в эндпоинте:
    - DELETE /api/tweets/{tweet_id} - удалить твит
    """

    stmt = (
        select(Tweets)
        .where(Tweets.tweet_id == tweet_id)
        .options(joinedload(Tweets.medias))
    )

    db_response: Result = await session.execute(stmt)
    tweet: Tweets | None = db_response.unique().scalar_one_or_none()

    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tweet '{tweet_id}' not found!",
        )

    if tweet.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You don't have permission "
            f"to delete the tweet '{tweet_id}'!",
        )

    if tweet.medias:
        for media in tweet.medias:
            media_path = Path(media.media_path)
            await delete_media(file_path=media_path)

    await session.delete(tweet)
    await session.commit()
