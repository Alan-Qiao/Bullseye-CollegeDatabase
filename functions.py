import pickle
import re

from lxml import html
import requests
import csv
from pathlib import Path
from college import College, Major

csc_key = 'YeY63i2SaSZU07HY5w01KJGjlB4S4O26JgnhTKAT'
college_list = {}
college_access = {}


def main():
    global college_list, college_access
    # '''
    csv_read(3)
    for coll in college_access:
        add_college(coll)
    # '''
    # college_list = load_obj(Path('college/college_list.pickle'))
    # '''
    for school in college_list:
        csc_grab(school)
        cpx_grab(school)
        cdt_grab(school)
        save_obj(college_list, Path('college/college_list.pickle'))
        print(school + ' Updated')
    
    save_obj(college_list, Path('college/college_list.pickle'))
    csv_write(1)
    print('Data for Colleges Saved to CSV')
    csv_write(2)
    print('Data for Majors Saved to CSV')
    # '''


def add_college(college_name):
    """
    Create a new College Object and add it to list of colleges
    :param str college_name: Name of College
    """
    global college_list
    clg = college_access[college_name]
    college_list[college_name] = College(clg['name'], clg['csc_name'], clg['nch_name'], clg['cpx_name'], clg['cdt_name'])


def csc_grab(college_name):
    """
    Scrap College Info from CollegeScoreCard
    :param str college_name: Name of College
    """
    global college_list
    url = 'https://api.data.gov/ed/collegescorecard/v1/schools.json'
    payload = {
        'api_key': csc_key,
        'id': college_list[college_name].csc,
        'fields': ','.join([
            'school.city', 'school.state', 'school.locale', 'school.ownership', 'school.carnegie_undergrad',
            'latest.cost.attendance.academic_year', 'latest.cost.net_price.public.by_income_level.0-30000',
            'latest.cost.net_price.public.by_income_level.30001-48000', 'latest.cost.net_price.public.by_income_level.48001-75000',
            'latest.cost.net_price.public.by_income_level.75001-110000', 'latest.cost.net_price.public.by_income_level.110001-plus',
            'latest.cost.net_price.private.by_income_level.0-30000', 'latest.cost.net_price.private.by_income_level.30001-48000',
            'latest.cost.net_price.private.by_income_level.48001-75000', 'latest.cost.net_price.private.by_income_level.75001-110000',
            'latest.cost.net_price.private.by_income_level.110001-plus', 'latest.aid.median_debt.completers.overall',
            'latest.student.size', 'latest.student.demographics.men', 'latest.student.demographics.women',
            'latest.student.demographics.race_ethnicity.white', 'latest.student.demographics.race_ethnicity.black',
            'latest.student.demographics.race_ethnicity.hispanic', 'latest.student.demographics.race_ethnicity.asian',
            'latest.student.demographics.race_ethnicity.aian', 'latest.student.demographics.race_ethnicity.nhpi',
            'latest.student.demographics.race_ethnicity.two_or_more', 'latest.student.demographics.race_ethnicity.non_resident_alien',
            'latest.student.demographics.race_ethnicity.unknown', 'latest.student.demographics.race_ethnicity.asian_pacific_islander',
            'latest.student.share_lowincome', 'latest.student.share_middleincome', 'latest.student.share_highincome',
            'latest.programs.cip_4_digit.title', 'latest.programs.cip_4_digit.credential.level',
            'latest.programs.cip_4_digit.debt.parent_plus.all.eval_inst.average', 'latest.earnings.6_yrs_after_entry.working_not_enrolled.mean_earnings'
        ])
    }
    resp = requests.get(url, params=payload).json()
    data = resp.get('results')[0]

    college_list[college_name].location = ','.join([data.get('school.city'), data.get('school.state')])
    college_list[college_name].set_locale(data.get('school.locale'))
    college_list[college_name].set_inst_type(data.get('school.ownership'))
    college_list[college_name].prog_len = '2 years' if data.get('school.carnegie_undergrad') <= 4 else '4 years'
    college_list[college_name].avg_cost = data.get('latest.cost.attendance.academic_year')
    college_list[college_name].set_ac_to_inc(data)
    college_list[college_name].med_post_grad_debt = int(data.get('latest.aid.median_debt.completers.overall'))
    college_list[college_name].tot_population = data.get('latest.student.size')
    college_list[college_name].set_gender_pct(data.get('latest.student.demographics.men'), data.get('latest.student.demographics.women'))
    college_list[college_name].set_ethnicity_pct(data.get('latest.student.demographics.race_ethnicity.white'),
                                                 data.get('latest.student.demographics.race_ethnicity.black'),
                                                 data.get('latest.student.demographics.race_ethnicity.hispanic'),
                                                 data.get('latest.student.demographics.race_ethnicity.asian'),
                                                 data.get('latest.student.demographics.race_ethnicity.aian'),
                                                 data.get('latest.student.demographics.race_ethnicity.nhpi'),
                                                 data.get('latest.student.demographics.race_ethnicity.two_or_more'),
                                                 data.get('latest.student.demographics.race_ethnicity.unknown'))
    college_list[college_name].international_pct = str(int(data.get('latest.student.demographics.race_ethnicity.non_resident_alien')*100))+'%'
    college_list[college_name].set_social_econ_pct(data)
    college_list[college_name].get_majors(data.get('latest.programs.cip_4_digit'))
    college_list[college_name].avg_ft_salary = 'Mean Full-Time Income 2 Years After Graduation: '+str(data.get('latest.earnings.6_yrs_after_entry.working_not_enrolled.mean_earnings'))


'''
def nch_grab(college_name):
    global college_list
    url = 'https://www.niche.com/colleges/'+college_list[college_name].nch+'/'
    tree = get_page(url)
    pass
'''


def cpx_grab(college_name):
    """
    Scrape College Information from Cappex
    :param str college_name: Name of College
    """
    global college_list
    url = 'https://www.cappex.com/colleges/'+college_list[college_name].cpx+'/'

    tree = get_page(url, 'academics')
    college_list[college_name].set_stu_to_fac(tree.xpath('//*[@id="block-fingerprint-content"]/div/article/div[2]/div/div[2]/section[1]/div[3]/div[1]/div[2]/text()'))

    tree = get_page(url, 'admissions')
    college_list[college_name].set_sat_mid_range(*tree.xpath('//*[@id="block-fingerprint-content"]/div/article/div[2]/div/div[2]/section[5]/div[3]/div/div//div[@class="bar-bg-big-percentage"]/div[@class]/text()'))
    college_list[college_name].set_stand_test_sub(next(iter(tree.xpath('//*[@id="block-fingerprint-content"]/div/article/div[2]/div/div[2]/section[4]/div[2]/div[2]/div/div[1]/div/text()')), None),
                                                  next(iter(tree.xpath('//*[@id="block-fingerprint-content"]/div/article/div[2]/div/div[2]/section[4]/div[2]/div[1]/div/div[1]/div/text()')), None))
    college_list[college_name].fin_on_adm = tree.xpath('//*[@id="block-fingerprint-content"]/div/article/div[2]/div/div[2]/section[2]/div[1]/div[1]/h3/text()')[0][1:-1]
    college_list[college_name].set_appl_dl(tree.xpath('//*[@id="block-fingerprint-content"]/div/article/div[2]/div/div[2]/section[4]/div[1]/table/tbody/tr/td/text()'))

    tree = get_page(url, 'campus-life')
    college_list[college_name].set_sports_teams(tree.xpath('//*[@id="block-fingerprint-content"]/div/article/div[2]/div/div[2]/section[3]/div[2]/div[2]/div[1]/div[2]/ul/*/text()'),
                                                tree.xpath('//*[@id="block-fingerprint-content"]/div/article/div[2]/div/div[2]/section[3]/div[2]/div[2]/div[2]/div[2]/ul/*/text()'))

    tree = get_page(url, 'after-graduation')
    college_list[college_name].set_outcomes(tree.xpath('//*[@id="block-fingerprint-content"]/div/article/div[2]/div/div[2]/section/div[1]/div[2]/div[text()="Employed"]/following-sibling::div[2]/div/text()'))
    college_list[college_name].top_employers = ', '.join(tree.xpath('//*[@id="block-fingerprint-content"]/div/article/div[2]/div/div[2]/section/div[2]/div[2]/div[2]/div/*/text()'))
    college_list[college_name].top_sectors = ', '.join(tree.xpath('//*[@id="block-fingerprint-content"]/div/article/div[2]/div/div[2]/section/div[2]/div[3]/div[2]/div/*/text()'))


def cdt_grab(college_name):
    """
    Scrape College Information from CollegeData
    :param str college_name: Name of College
    """
    global college_list
    url = 'https://www.collegedata.com/college-search/'+college_list[college_name].cdt

    tree = get_page(url)
    college_list[college_name].full_cost = {tree.xpath('//*[@id="app-container"]/div/div/div[2]/div[1]/div/div[2]/div[2]/div[3]/div/div[position()<4]//div[@class="TitleValue_title__2-afK"]/text()')[x]:
                                            ', '.join(tree.xpath('//*[@id="app-container"]/div/div/div[2]/div[1]/div/div[2]/div[2]/div[3]/div[position()='+str(x+1)+']//div[@class="TitleValue_value__1JT0d"]/text()'))
                                            for x in range(3)}
    tree = get_page(url, '/campus-life')
    college_list[college_name].set_weather(tree.xpath('//*[@id="app-container"]/div/div/div[2]/div[1]/div/div[1]/div/div[3]/div/div/div/div[text()="Avg Low In Jan"]/following-sibling::div/text()')[0],
                                           tree.xpath('//*[@id="app-container"]/div/div/div[2]/div[1]/div/div[1]/div/div[3]/div/div/div/div[text()="Avg High In Sep"]/following-sibling::div/text()')[0],
                                           tree.xpath('//*[@id="app-container"]/div/div/div[2]/div[1]/div/div[1]/div/div[3]/div/div/div/div[text()="Rainy Days / Year"]/following-sibling::div/text()')[0])
    college_list[college_name].res_pct = tree.xpath('//*[@id="app-container"]/div/div/div[2]/div[1]/div/div[2]/div[2]/div[3]/div/div[3]/div/div[2]/text()')[0]
    college_list[college_name].set_res_rqd(tree.xpath('//*[@id="app-container"]/div/div/div[2]/div[1]/div/div[2]/div[2]/div[3]/div/div/div/div[text()="Housing Requirements"]/following-sibling::div/text()'))
    college_list[college_name].personal_care = {tree.xpath('//*[@id="app-container"]/div/div/div[2]/div[1]/div/div[4]/div[2]/div[3]/div//div[@class="TitleValue_title__2-afK"]/text()')[x]:
                                                tree.xpath('//*[@id="app-container"]/div/div/div[2]/div[1]/div/div[4]/div[2]/div[3]/div//div[@class="TitleValue_value__1JT0d"]/text()')[x]
                                                for x in range(len(tree.xpath('//*[@id="app-container"]/div/div/div[2]/div[1]/div/div[4]/div[2]/div[3]/div//div[@class="TitleValue_title__2-afK"]/text()')))}

    tree = get_page(url, '/money-matters')
    college_list[college_name].full_cost.update({tree.xpath('//*[@id="app-container"]/div/div/div[1]/div[3]/div/div/div/div[5]/div[position()>2]//div[@class="StatLine_label__1Kxkv"]/text()')[x]:
                                                 tree.xpath('//*[@id="app-container"]/div/div/div[1]/div[3]/div/div/div/div[5]/div[position()>2]//div[@class="StatLine_value__1ASq0"]/text()')[x]
                                                 for x in range(2)})
    college_list[college_name].set_aid(tree.xpath('//*[@id="app-container"]/div/div/div[2]/div[1]/div/div[3]/div[2]/div[3]/div/div/div//*[text()]'))

    tree = get_page(url, '/admission')
    college_list[college_name].set_adm_stats(tree.xpath('//*[@id="app-container"]/div/div/div[2]/div[1]/div/div[4]/div[2]/div[3]/div/div[1]/div/div[2]/text()')[0],
                                             tree.xpath('//*[@id="app-container"]/div/div/div[2]/div[1]/div/div[4]/div[2]/div[3]/div/div[2]/div/div[2]/text()')[0])
    college_list[college_name].interview = tree.xpath('//*[@id="app-container"]/div/div/div[2]/div[1]/div/div[2]/div[2]/div[3]/div/div/div/div[text()="Interview"]/following-sibling::div/text()')[0]
    college_list[college_name].set_stand_test(tree.xpath('//*[@id="app-container"]/div/div/div[2]/div[1]/div/div[1]/div/div[3]/div/div/div/table/tbody/tr/td[text()="SAT or ACT"]/../../tr/td[2]/text()'))
    college_list[college_name].set_act_mid_range(tree.xpath('//*[@id="app-container"]/div/div/div[2]/div[1]/div/div[4]/div[2]/div[3]/div/div//h6[contains(text(), "ACT Scores")]/../../following-sibling::div[1]/div/div[1]/text()')[0])

    tree = get_page(url, '/academics')
    college_list[college_name].spec_prog = tree.xpath('//*[@id="app-container"]/div[1]/div/div[2]/div[1]/div/div[1]/div/div[3]/div/div[4]/div/text()')[1:]
    college_list[college_name].acad_supp = {tree.xpath('//*[@id="app-container"]/div[1]/div/div[2]/div[1]/div/div[6]/div[2]/div[3]/div/div/div/div[@class="TitleValue_title__2-afk"/text()')[x]:
                                            tree.xpath('//*[@id="app-container"]/div[1]/div/div[2]/div[1]/div/div[6]/div[2]/div[3]/div/div/div/div[@class="TitleValue_value__1JT0d"/text()')[x]
                                            for x in range(len(tree.xpath('//*[@id="app-container"]/div[1]/div/div[2]/div[1]/div/div[6]/div[2]/div[3]/div/div/div/div[@class="TitleValue_title__2-afk"]/text()')))}


def get_page(src, suffix=''):
    """
    Return HTML requested web page
    :param str src: Main URL of site
    :param str suffix: Additional parameters or page specifiers
    :return: HTML of site
    """
    page = requests.get(src+suffix, headers={'User-Agent': 'Mozilla/5.0'})
    if not page.ok:
        print(page.status_code)
        save_obj(college_list, Path('college/college_data.pickle'))
        return None
    return html.fromstring(page.content)


def csv_read(opt):
    """
    Read CSV files to global variables. Reads from 3 predefined options.
    1. Read Data of Colleges from saved csv
    2. Read Data of majors from saved csv
    3. Read list of Colleges to be considered from csv
    :param int opt: csv file option
    """
    global college_access, college_list
    if opt == 1:
        fieldnames = ['name', 'csc', 'nch', 'cpx', 'cdt', 'location', 'inst_type', 'locale', 'prog_len', 'weather',
                      'full_cost', 'avg_cost', 'ac_to_inc', 'aid', 'med_post_grad_debt', 'adm_rate', 'tot_appl',
                      'tot_adm', 'essay', 'interview', 'stand_test', 'stand_test_sub', 'sat_mid_range', 'act_mid_range',
                      'appl_dl', 'fin_on_adm', 'tot_population', 'class_population', 'stu_to_fac', 'gender_pct',
                      'ethnicity_pct', 'international_pct', 'social_econ_pct', 'sub_school', 'spec_prog', 'acad_supp',
                      'res_pct', 'res_rqd', 'meal_plan', 'clubs', 'sports_teams', 'personal_care', 'outcomes',
                      'avg_ft_salary', 'top_employers', 'top_sectors']
        try:
            csvfile = open(Path('college/college_data.csv'), 'r', newline='', encoding='utf-8')
        except UnicodeDecodeError:
            csvfile = open(Path('college/college_data.csv'), 'r', newline='', encoding='ISO-8859-1')
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        next(reader)
        for row in reader:
            college_list[row['name']] = College(**row)
        csvfile.close()
        return
    if opt == 2:
        fieldnames = ['school', 'name', 'count', 'mean_debt', 'career']
        try:
            csvfile = open(Path('college/major_data.csv'), 'r', newline='', encoding='utf-8')
        except UnicodeDecodeError:
            csvfile = open(Path('college/major_data.csv'), 'r', newline='', encoding='ISO-8859-1')
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        next(reader)
        for row in reader:
            if not isinstance(college_list[row['school']]['majors'], list):
                college_list[row['school']]['majors'] = []
            college_list[row['school']]['majors'].append(Major(**row))
        csvfile.close()
        return
    if opt == 3:
        with open('school_access_name.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                college_access[row['name']] = row
        return


def csv_write(opt):
    """
    Write college or major data to csv file. Two predefined options.
    1. Write College Data to file
    2. Write Major Data to file
    :param int opt: csv file option
    """
    global college_list
    if opt == 1:
        fieldnames = ['Name', 'csc', 'nch', 'cpx', 'cdt', 'Location', 'Institution Type', 'Locale', 'Program Length',
                      'Weather', 'Full Cost', 'Average Cost', 'Average Cost by Income', 'Aid Available',
                      'Median Debt at Completion', 'Admission Rate', 'Total Applicants', 'Total Admitted',
                      'Essays Questions', 'Interview Requirement', 'Standardized Testing Requirements',
                      'Standardized Testing Submission Rate', 'SAT Mid-Range', 'ACT Mid-Range', 'Application Deadlines',
                      'Financial Consideration on Admission', 'Undergraduate Population', 'Class Population',
                      'Student Faculty Ratio', 'Gender Breakdown', 'Ethnicity Breakdown',
                      'Percentage International Students', 'Socio-Economic Breakdown', 'Sub-schools',
                      'Special Programs', 'Academic Support Services', 'Percentage Living in Residence',
                      'Residence Requirement', 'Meal Plan', 'Clubs', 'Sports Teams', 'Personal Support Services',
                      'Graduation Outcomes', 'Average Full-time Salary', 'Top Employers', 'Top Employment Sectors']
        with open(Path('college/college_data.csv'), 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            for college in college_list.values():
                row = college.to_csv_row()
                writer.writerow(row)
        return
    if opt == 2:
        fieldnames = ['School', 'Major Name', 'Popularity', 'Mean Federal Loan Debt', 'Top Careers']
        with open(Path('college/major_data.csv'), 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            for college in college_list.values():
                for major in college.majors:
                    writer.writerow(vars(major).values())


def load_obj(filename):
    """
    Return object loaded from pickle file
    :param Path filename: path to pickle file
    :return: Loaded Object
    """
    with open(filename, 'rb') as file:
        obj = pickle.load(file)
    return obj


def save_obj(obj, filename):
    """
    Write object to pickle file
    :param obj: object to be written
    :param Path filename: path of destination pickle file
    """
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, 4)


if __name__ == "__main__":
    main()
