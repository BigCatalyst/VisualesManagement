from celery import shared_task

from tasks.views import movies_imdb, movies_filmaffinity, series_imdb, \
    games_rawg_io, review_empty_fields, actors_imdb, author_coveralia, album_coveralia


@shared_task
def update_movies_weekly_task():
    """Update movies to celery every week."""
    movies_imdb()
    movies_filmaffinity()
    pass


@shared_task
def update_series_weekly_task():
    """Update series to celery every week."""
    actors_imdb()
    series_imdb()


@shared_task
def update_games_weekly_task():
    """Update games to celery every week."""
    games_rawg_io()
    author_coveralia()
    album_coveralia()
    


@shared_task
def review_empty_fields_task():
    """Update games to celery every week."""
    review_empty_fields()
    
