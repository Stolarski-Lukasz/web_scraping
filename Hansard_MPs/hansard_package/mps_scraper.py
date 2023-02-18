import re
import requests
from bs4 import BeautifulSoup
import pandas as pd


class MpsScraper():

    def __init__(self):
        self.person_elements = None
        self.person_name_list = []
        self.person_honorific_prefix_list = []
        self.person_given_name_list = []
        self.person_family_name_list = []
        self.person_title_in_lords_list = []
        self.person_link_list = []
        self.person_life_span_list = []
        self.person_birth_list = []
        self.person_death_list = []
        self.person_title_list = []
        self.person_gender_list = []
        self.person_service_beginning_list = []
        self.person_service_ending_list = []
        self.person_constituency_names_listoflists = []
        self.person_service_spans_listoflists = []
        self.person_name = None
        self.person_link = None
        self.person_soup_html = None
        self.people_dict = {}

    def get_person_elements(self, base_url, letter):
        print(letter)
        url_letter = base_url + letter
        raw_html = requests.get(url_letter)
        soup_html = BeautifulSoup(raw_html.text, "html.parser")
        self.person_elements = soup_html.find_all("li", class_="person")


    def get_name_link_lifespan_birth_death(self, element):
        anchor = element.a
        person_name = str(anchor.string)
        print(person_name)
        self.person_name = person_name
        self.person_name_list.append(person_name)
        person_link = str(anchor["href"])
        self.person_link = person_link
        self.person_link_list.append(person_link)
        try:
            span = element.span
            person_life_span = str(span.string)
            self.person_life_span_list.append(person_life_span)
            dates = re.findall(r'\d{4,4}', person_life_span)
            if len(dates) > 1:
                person_birth = dates[0]
                person_death = dates[1]
            else:
                date_index = re.search(r'\d{4,4}', person_life_span)
                date_end_index = date_index.end()
                hyphen_index = re.search(r'-', person_life_span)
                hyphen_start_index = hyphen_index.start()
                if date_end_index < hyphen_start_index:
                    person_birth = dates[0]
                    person_death = "unknown"
                else:
                    person_birth = "unknown"
                    person_death = dates[0]
            self.person_birth_list.append(person_birth)
            self.person_death_list.append(person_death)
        except AttributeError:
            self.person_birth_list.append("unknown")
            self.person_death_list.append("unknown")

    def get_title_gender(self, person_title_gender):
        person_title_gender = pd.read_table(person_title_gender)
        person_name = str(self.person_name)
        parenthesis_contents = re.search(r"\((.+)\)", person_name)
        try:
            person_title = parenthesis_contents.group(1)
        except AttributeError:
            person_title = "unknown"
        self.person_title_list.append(person_title)

        pd_counter = 0
        for title in person_title_gender.person_title.values:
            if title == person_title:
                person_gender = person_title_gender.loc[pd_counter,
                                                                    'person_gender']
                pd_counter += 1
                break
            else:
                pd_counter += 1
        self.person_gender_list.append(person_gender)

    def get_constituency_servicespan(self, base_url):
        person_url = base_url + self.person_link
        person_raw_html = requests.get(person_url)
        person_soup_html = BeautifulSoup(person_raw_html.text, "html.parser")
        self.person_soup_html = person_soup_html
        person_constituency_iterator = person_soup_html.find_all(
            "li", class_="constituency")
        person_constituency_elements_list = list(person_constituency_iterator)
        person_constituency_names_list = []
        person_service_spans_list = []
        person_constituency_elements_list_len = len(
            person_constituency_elements_list)
        counter = 1
        if person_constituency_elements_list_len > 0:
            for person_constituency_element in person_constituency_elements_list:
                person_constituency_name = person_constituency_element.a.string
                person_constituency_names_list.append(str(person_constituency_name))
                service_span = person_constituency_element.contents[1]
                person_service_spans_list.append(str(service_span))
                if counter == 1:
                    service_dates = re.findall(r'\d{4,4}', str(service_span))
                    service_beginning = service_dates[0]
                    self.person_service_beginning_list.append(str(service_beginning))
                try:
                    if counter == len(person_constituency_elements_list):
                        service_dates = re.findall(r'\d{4,4}', str(service_span))
                        service_ending = service_dates[1]
                        self.person_service_ending_list.append(str(service_ending))
                except AttributeError:
                    self.person_service_ending_list.append('unknown')
                counter += 1
            self.person_constituency_names_listoflists.append(
                person_constituency_names_list)
            self.person_service_spans_listoflists.append(person_service_spans_list)
        else:
            self.person_constituency_names_listoflists.append(['unknown'])
            self.person_service_spans_listoflists.append(['unknown'])
            self.person_service_beginning_list.append('unknown')
            self.person_service_ending_list.append('unknown')

    def get_honorificprefix_givenname_familyname_titlesinlords(self):
        try:
            person_honorific_prefix = self.person_soup_html.find(
                "span", class_="honorific-prefix")
            person_honorific_prefix = str(person_honorific_prefix.string)
            self.person_honorific_prefix_list.append(person_honorific_prefix)
        except AttributeError:
            self.person_honorific_prefix_list.append('unknown')
        try:
            person_given_name = self.person_soup_html.find(
                "span", class_="given-name")
            person_given_name = str(person_given_name.string)
            self.person_given_name_list.append(person_given_name)
        except AttributeError:
            self.person_given_name_list.append("unknown")
        try:
            person_family_name = self.person_soup_html.find(
            "span", class_="family-name")
            person_family_name = str(person_family_name.string)
            self.person_family_name_list.append(person_family_name)
        except AttributeError:
            self.person_family_name_list.append("unknown")
        try:
            person_title_in_lords = self.person_soup_html.find(
                "li", class_="lords-membership")
            person_title_in_lords = str(person_title_in_lords.string)
            self.person_title_in_lords_list.append(person_title_in_lords)
        except AttributeError:
            self.person_title_in_lords_list.append('unknown')

    def prepare_dict_forexport(self):
        self.people_dict['name'] = self.person_name_list
        self.people_dict['title'] = self.person_title_list
        self.people_dict['honorific_prefix'] = self.person_honorific_prefix_list
        self.people_dict['given_name'] = self.person_given_name_list
        self.people_dict['family_name'] = self.person_family_name_list
        self.people_dict['title_in_lords'] = self.person_title_in_lords_list
        self.people_dict['link'] = self.person_link_list
        self.people_dict['gender'] = self.person_gender_list
        self.people_dict['life_span'] = self.person_life_span_list
        self.people_dict['birth'] = self.person_birth_list
        self.people_dict['death'] = self.person_death_list
        self.people_dict['constituency'] = self.person_constituency_names_listoflists
        self.people_dict['service_span'] = self.person_service_spans_listoflists
        self.people_dict['service_beginning'] = self.person_service_beginning_list
        self.people_dict['service_ending'] = self.person_service_ending_list

