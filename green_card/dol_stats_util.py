import urllib
from bs4 import BeautifulSoup
import json
from re import sub
from decimal import Decimal
import codecs

ICERT_URL ="http://icert.doleta.gov/index.cfm?event=ehLCJRExternal.dspCert&doc_id=3&visa_class_id=6&id={}"

def get_data(soup, text):
    try:
        return soup.find(text=text).parent.parent.p.string.strip() if soup is not None else ""
    except Exception as e:
        return ""

def get_offered_wage(soup):
    try:
        money = soup.find_all(style="color: #000")[0].parent.text.strip().split()[2]
        return  int(Decimal(sub(r'[^\d.]', '', money)).to_integral_value())
    except Exception as e:
        return 0

def get_highest_degree(alien_information):
    try:
        return alien_information.find(text="11. Education: highest level achieved relevant to the requested occupation:").parent.parent.find_all(
        alt="checked")[0].string
    except Exception as e:
        return None

def get_icert_data(html):
    try:
        soup = BeautifulSoup(html)
        offered_wage = get_offered_wage(soup)

        alien_information = soup.find(
            text="J. Alien Information (This section must be filled out. This information must be different from the agent or attorney information listed in Section E).").parent.parent.parent

        citizenship = get_data(alien_information,
                               "5. Country of citizenship") #alien_information.find(text="5. Country of citizenship").parent.parent.p.string.strip()
        country_of_birth = get_data(alien_information,
                                    "6. Country of birth") #alien_information.find(text="6. Country of birth").parent.parent.p.string.strip()
        class_of_admission = get_data(alien_information,
                                      "8. Class of admission")# alien_information.find(text="8. Class of admission").parent.parent.p.string.strip()
        highest_degree = get_highest_degree(alien_information)

        field_of_study = get_data(alien_information,
                                  "12. Specify major field(s) of study")# alien_information.find(text="12. Specify major field(s) of study").parent.parent.p.string.strip()
        graduation_date = get_data(alien_information,
                                   "13. Year relevant education completed")# alien_information.find(text="13. Year relevant education completed").parent.parent.p.string.strip()
        university = get_data(alien_information,
                              "14. Institution where relevant education specified in question 11 was received")# alien_information.find(text="14. Institution where relevant education specified in question 11 was received").parent.parent.p.string.strip()

        return {"offered_wage": offered_wage, "citizenship": citizenship, "country_of_birth": country_of_birth,
                "class_of_admission": class_of_admission, "highest_degree": highest_degree,
                "field_of_study": field_of_study, "graduation_date": graduation_date, "university": university}
    except Exception:

        return None

if __name__ == '__main__':
    employers = {"rubicon":"http://dolstats.com/searchAjax?&case-types=ALL&employer-name=THE+RUBICON+PROJECT",
                 "microsoft":"http://dolstats.com/searchAjax?&case-types=ALL&employer-name=MICROSOFT+CORPORATION",
                 "facebook":"http://dolstats.com/searchAjax?&case-types=ALL&employer-name=FACEBOOK",
                 "yahoo":"http://dolstats.com/searchAjax?&case-types=ALL&employer-name=YAHOO",
                 "salesforce":"http://dolstats.com/searchAjax?&case-types=ALL&employer-name=SALESFORCE",
                 "qualcomm":"http://dolstats.com/searchAjax?&case-types=ALL&employer-name=QUALCOMM",
                 "oracle":"http://dolstats.com/searchAjax?&case-types=ALL&employer-name=ORACLE",
                 "citigroup":"http://dolstats.com/searchAjax?&case-types=ALL&employer-name=CITIGROUP",
                 "bank_of_america":"http://dolstats.com/searchAjax?&case-types=ALL&employer-name=BANK+OF+AMERICA",
                 "intel":"http://dolstats.com/searchAjax?&case-types=ALL&employer-name=INTEL",
                 "demand_media":"http://dolstats.com/searchAjax?&case-types=ALL&employer-name=DEMAND+MEDIA",
                 "amazon":"http://dolstats.com/searchAjax?&case-types=ALL&employer-name=AMAZON",
                 "apple":"http://dolstats.com/searchAjax?&case-types=ALL&employer-name=APPLE",
                 "adconion":"http://dolstats.com/searchAjax?&case-types=ALL&employer-name=ADCONION",
                 "openx":"http://dolstats.com/searchAjax?&case-types=ALL&employer-name=OPENX",
                 "cognizant":"http://dolstats.com/searchAjax?&case-types=ALL&employer-name=COGNIZANT+TECHNOLOGY+SOLUTIONS+US+CORPORATION",
                 "infosys":"http://dolstats.com/searchAjax?&case-types=ALL&employer-name=INFOSYS",
                 "wipro":"http://dolstats.com/searchAjax?&case-types=ALL&employer-name=WIPRO+LIMITED",
                 "ebay":"http://dolstats.com/searchAjax?&case-types=ALL&employer-name=EBAY"}

    for employer, url in employers.items():

        applicants = json.loads(urllib.urlopen(url).read())['result']

        print "processing for ", employer
        with codecs.open("%s_data.json"%employer,"wb") as write_file:
            skipped_count =0
            count =0
            for applicant in applicants:

                if applicant['cT'] == "PERM" and applicant['cR'] == "Certified":

                    count+=1
                    applicant_info = dict(applicant.items() + get_icert_data(urllib.urlopen(ICERT_URL.format(applicant['id'])).read()).items())
                    write_file.write("%s\n"%json.dumps(applicant_info))
                else:
                    skipped_count +=1

                print "Processed ", count, skipped_count



