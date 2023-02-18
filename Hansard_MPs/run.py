from hansard_package.mps_scraper import MpsScraper
from hansard_package.results_saver import ResultsSaver


if __name__ == "__main__":
    # setting up environment
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z']
    base_url = "https://api.parliament.uk/historic-hansard/people/"
    
    # web scraping
    mps_scraper = MpsScraper()
    for letter in letters:
        mps_scraper.get_person_elements(base_url=base_url, letter=letter)
        for element in mps_scraper.person_elements:
            mps_scraper.get_name_link_lifespan_birth_death(element=element)
            mps_scraper.get_title_gender(person_title_gender='data/people_gender.tsv')
            mps_scraper.get_constituency_servicespan(base_url=base_url)
            mps_scraper.get_honorificprefix_givenname_familyname_titlesinlords()
            mps_scraper.prepare_dict_forexport()

    # saving results
    results_saver = ResultsSaver(mps_scraper.people_dict)
    results_saver.save_as_pickle("results/mps.pickle")
    results_saver.save_as_tsv("results/mps.tsv")



