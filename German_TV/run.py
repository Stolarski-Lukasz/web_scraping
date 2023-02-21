import datetime
import settings as s
from tv_module import TvScraper, TvFilter, TvResultsSaver


if __name__ == "__main__":
    today = datetime.datetime.now()
    today = str(today)[:10]

    # web scraping
    tv_scraper = TvScraper()
    page = 1
    while page <= s.MAX_PAGES:
        tv_scraper.process_html(page=page)
        tv_scraper.get_titles()
        tv_scraper.get_genres()
        tv_scraper.get_times()
        tv_scraper.get_channels()
        page += 1

    # filtering MY_FREE_CHANNELS and saving the results
    tv_filter = TvFilter()
    tv_filter.filter_my_channels(channels_list=tv_scraper.channels_list, 
                                titles_list=tv_scraper.titles_list,
                                genres_list=tv_scraper.genres_list,
                                times_list=tv_scraper.times_list)

    tv_results_saver = TvResultsSaver()
    tv_results_saver.save_as_df(final_titles_list=tv_filter.final_titles_list,
                                final_genres_list=tv_filter.final_genres_list,
                                final_channels_list=tv_filter.final_channels_list,
                                final_times_list=tv_filter.final_times_list,
                                today=today,
                                df_name="all_series")

    # additional filtering MY_SERIES and saving the results
    tv_filter.filter_my_series()
    tv_results_saver.save_as_df(final_titles_list=tv_filter.my_series_titles,
                                final_genres_list=tv_filter.my_series_genres,
                                final_channels_list=tv_filter.my_series_channels,
                                final_times_list=tv_filter.my_series_times,
                                today=today,
                                df_name="my_series")
