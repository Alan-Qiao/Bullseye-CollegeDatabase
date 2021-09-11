class College:
    def __init__(self, name, csc, nch, cpx, cdt, location=None, inst_type=None, locale=None, prog_len=None, weather=None,
                 full_cost=None, avg_cost=None, ac_to_inc=None, aid=None, has_aid=None, med_post_grad_debt=None,
                 adm_rate=None, tot_appl=None, tot_adm=None, essay=None, interview=None, stand_test=None,
                 stand_test_sub=None, sat_mid_range=None, act_mid_range=None, appl_dl=None, fin_on_adm=None,
                 tot_population=None, class_population=None, stu_to_fac=None, gender_pct=None, ethnicity_pct=None,
                 international_pct=None, social_econ_pct=None, majors=None, sub_school=None, spec_prog=None,
                 acad_supp=None, res_pct=None, res_rqd=None, meal_plan=None, clubs=None, sports_teams=None,
                 personal_care=None, outcomes=None, avg_ft_salary=None, top_employers=None, top_sectors=None):

        self.name = name  # 0 college name
        self.csc = csc  # 1 college scorecard id
        self.nch = nch  # 2 niche id
        self.cpx = cpx  # 3 cappex id
        self.cdt = cdt  # 4 college data id

        self.location = location  # 5 location
        self.inst_type = inst_type  # 6 institution type
        self.locale = locale  # 7 locale (city size, rural size)
        self.prog_len = prog_len  # 8 program length
        self.weather = weather  # 9 general weather, temperature range/rain days

        self.full_cost = full_cost  # 10 full cost of attendance
        self.avg_cost = avg_cost  # 11 average cost of attendance (Financial Aid adjusted)
        self.ac_to_inc = ac_to_inc  # 12 Average Cost by Income Group
        self.aid = aid  # 13  # Merit, Grant, Loan Aid
        self.has_aid = has_aid  # Whether school offers Aid
        self.med_post_grad_debt = med_post_grad_debt  # 14 Median Post Graduation Debt

        self.adm_rate = adm_rate  # 15  # Admission Rate, includes breakdown
        self.tot_appl = tot_appl  # 16 Total Applicants
        self.tot_adm = tot_adm  # 17 Total Admitted
        self.essay = essay  # rqd  # 18 Essay Required?
        self.interview = interview  # 19 Interview Required?
        self.stand_test = stand_test  # 20 Standardize Testing Policy
        self.stand_test_sub = stand_test_sub  # 21  # % submitted stand_test
        self.sat_mid_range = sat_mid_range  # 22 SAT mid-range
        self.act_mid_range = act_mid_range  # 23 ACT mid-range
        self.appl_dl = appl_dl  # 24  # All application deadlines
        self.fin_on_adm = fin_on_adm  # 25  # FA policy: Need-blind, Need-based, etc.

        self.tot_population = tot_population  # 26 Total Population
        self.class_population = class_population  # 27 Size of previous admitted class
        self.stu_to_fac = stu_to_fac  # 28 Student to Faculty Ratio
        self.gender_pct = gender_pct  # 29 Gender Ratio
        self.ethnicity_pct = ethnicity_pct  # 30 Enthnicity Breakdown
        self.international_pct = international_pct  # 31 Percent International Students
        self.social_econ_pct = social_econ_pct  # 32 Social Economic Class Breakdown

        self.majors = majors # Available Majors
        self.sub_school = sub_school  # 33 Subsidiary Schools Unimplemented
        self.spec_prog = spec_prog  # 34 Special Programs Offered
        self.acad_supp = acad_supp  # 35 Academic Support Available

        self.res_pct = res_pct  # 36 Percent living in Residence
        self.res_rqd = res_rqd  # 37 Residence requirement
        self.meal_plan = meal_plan  # 38  NA Meal Plan Availability
        self.clubs = clubs  # 39 Clubs
        self.sports_teams = sports_teams  # 40 Sports Teams
        self.personal_care = personal_care  # 41 Student Health Services

        self.outcomes = outcomes  # 42 Post-secondary Outcomes Breakdown
        self.avg_ft_salary = avg_ft_salary  # 43 Average Full-Time Salary 6 Years after Graduation
        self.top_employers = top_employers  # 44 Top Employers of Graduates
        self.top_sectors = top_sectors  # 45 Top Sectors that Employ Graduates

    def set_locale(self, locale):
        """
        Decipher College ScoreCard locale code into locale descriptions
        :param int locale: locale id
        """
        loc_dict = {11: 'City', 12: 'City', 13: 'City', 21: 'Suburb', 22: 'Suburb', 23: 'Suburb',
                    31: 'Town', 32: 'Town', 33: 'Town', 41: 'Rural', 42: 'Rural', 43: 'Rural'}
        self.locale = loc_dict.get(locale)

    def set_inst_type(self, ownership):
        """
        Decipher College ScoreCard Institutions code into institution ownership descriptions
        :param int ownership: ownership id
        """
        own_dict = {1: 'Public', 2: 'Private', 3: 'Private'}
        self.inst_type = own_dict.get(ownership)

    def set_ac_to_inc(self, data):
        """
        Reformat Average Cost of Attendance to Income Level data from College ScoreCard
        :param data: Input from College ScoreCard
        """
        ownership = 'public' if self.inst_type == 'Public' else 'private'
        self.ac_to_inc = {'Income 0-30k': data.get('latest.cost.net_price.{own}.by_income_level.0-30000'.format(own=ownership)),
                          'Income 30k-48k': data.get('latest.cost.net_price.{own}.by_income_level.30001-48000'.format(own=ownership)),
                          'Income 48k-75k': data.get('latest.cost.net_price.{own}.by_income_level.48001-75000'.format(own=ownership)),
                          'Income 75k-110k': data.get('latest.cost.net_price.{own}.by_income_level.75001-110000'.format(own=ownership)),
                          'Income 110k+': data.get('latest.cost.net_price.{own}.by_income_level.110001-plus'.format(own=ownership))}

    def set_weather(self, high, low, rain):
        """
        Reformat Weather Information into single string
        :param high: high temperature
        :param low: low temperature
        :param rain: rain days
        """
        self.weather = low + " average low in Jan, " + high + " average high in Sept, " + rain + " rainy days per year"

    def set_res_rqd(self, rqd):
        """
        Set Housing Requirements
        :param str rqd: List containing housing requirement strings
        """
        if len(rqd) < 1:
            self.res_rqd = "Not Reported"
        else:
            self.res_rqd = rqd[0]

    def set_aid(self, nodes):
        """
        Reformat element tree of aid elements from CollegeData to python list
        :param nodes: nodes of element tree containing aid information
        """
        aid = {}
        nodes_iter = iter(nodes)
        node = next(nodes_iter)
        while node.text != 'Employment':
            category = node.text
            offerings = {}
            node = next(nodes_iter)
            while node.get('class') != 'cd-web-h6':
                title = node.text
                programs = []
                node = next(nodes_iter)
                while (node.get('class') != 'TitleValue_title__2-afK') and (node.get('class') != 'cd-web-h6'):
                    programs.extend(node.text)
                    node = next(nodes_iter)
                offerings[title] = ', '.join(programs)
            aid[category] = offerings
        if 'State Loans' not in aid['Loans']:
            aid['Loans']['State Loans'] = 'None'
        if 'Other Loans' not in aid['Loans']:
            aid['Loans']['Other Loans'] = 'None'
        self.aid = aid

    def set_adm_stats(self, adm, pop):
        """
        Update admissions statistics with scraped information from CollegeData
        :param adm: Overall Admission Rate Info
        :param pop: Students Enrolled Info
        """
        '''
        rates = ['Overall: ' + stats[0].split()[0]]
        if stats[6] != '\xa0':
            if stats[6] == 'Not reported':
                rates.append('ED: Not Reported')
            else:
                rates.append('ED: ' + stats[6].split()[0])
        if stats[7] != '\xa0':
            if stats[7] == 'Not reported':
                rates.append('EA: Not Reported')
            else:
                rates.append('EA: ' + stats[7].split()[0])
        '''
        self.adm_rate = adm.split()[0] if adm != 'Not reported' else 'Not reported'
        self.tot_appl = adm.split()[2] if adm != 'Not reported' else 'Not reported'
        self.tot_adm = int(float(self.tot_appl.replace(',', '')) * (float(self.adm_rate[:-1])/100.))
        self.class_population = pop.split()[0] if pop != 'Not reported' else 'Not reported'

    def set_stu_to_fac(self, ratio):
        """
        Set the student to faculty ratio
        :param ratio: list containing student faculty ratio
        """
        if len(ratio) < 1:
            self.stu_to_fac = "Not Reported"
        else:
            self.stu_to_fac = str(ratio[0])

    def set_stand_test(self, policy):
        """
        Update Standardized Testing Policy
        :param policy: List of strings of standardized testing policies
        """
        if len(policy) == 4:
            self.stand_test = {'SAT or ACT': policy[0]+', '+policy[3].lower(), 'SAT Subject Test': policy[2]}
        elif len(policy) == 3:
            self.stand_test = {'SAT or ACT': policy[0]+', '+policy[2].lower(), 'SAT Subject Test': policy[1]}
        else:
            self.stand_test = {'SAT or ACT': 'Not Reported', 'SAT Subject Test': 'Not Reported'}

    def set_sat_mid_range(self, math25=0, math75=0, engl25=0, engl75=0):
        """
        Collect various SAT score range metric into single String description
        :param math25: math first percentile score.
        :param math75: math third percentile score.
        :param engl25: english first percentile score.
        :param engl75: english third percentile score.
        """
        low = int(math25) + int(engl25)
        high = int(math75) + int(engl75)
        self.sat_mid_range = str(low)+'-'+str(high)

    def set_act_mid_range(self, score):
        """
        Set ACT score range
        :param score: String containing ACT score summary
        """
        if score != "Not Reported":
            score = score.split()
            if score[1] == "average,":
                score = score[2]
            else:
                score = score[0]
        self.act_mid_range = score

    def set_stand_test_sub(self, sat_pct, act_pct):
        """
        Record percentage of students submitting SAT/ACT
        :param sat_pct: % Submitted SAT
        :param act_pct: % Submitted ACT
        """
        sat_pct = 'NA' if sat_pct is None else sat_pct[1:-1]
        act_pct = 'NA' if act_pct is None else act_pct[1:-1]
        sub_pct = ['Students Submitting SAT: '+sat_pct, 'Students Submitting ACT: '+act_pct]
        self.stand_test_sub = '\n'.join(sub_pct)

    def set_appl_dl(self, dl):
        """
        Set Application Deadlines of School
        :param dl: List of Deadlines
        """
        deadlines = []
        for i in range(len(dl), 2):
            deadlines.append(dl[i] + ': ' + dl[i+1])
        self.appl_dl = '\n'.join(deadlines)

    def set_gender_pct(self, m_dec, f_dec):
        """
        Set Gender Demographic Ratio
        :param m_dec: % Male in Decimals
        :param f_dec: % Female in Decimals
        """
        m_pct = int(m_dec*100) if isinstance(m_dec, float) else m_dec
        f_pct = int(f_dec*100) if isinstance(f_dec, float) else f_dec
        self.gender_pct = {'M': m_pct, 'F': f_pct}

    def set_ethnicity_pct(self, white, black, hispanic, asian, aian, nhpi, two_plus, unknown):
        """
        Set Ethnicity Breakdown
        :param white: Decimal Percent White
        :param black: Decimal Percent Black
        :param hispanic: Decimal Percent Hispanic
        :param asian: Decimal Percent Asian
        :param aian: Decimal Percent American Indian/Alaska Native
        :param nhpi: Decimal Percent of Native Hawaiian and Other Pacific Islander
        :param two_plus: Decimal Percent of identify with 2+ races
        :param unknown: Decimal Percent of Unknown
        """
        eth = [white, black, hispanic, asian, aian, nhpi, two_plus, unknown]
        for i in range(len(eth)):
            if (eth[i] is None) or (not isinstance(eth[i], float)):
                'Not Reported'
            else:
                eth[i] = round(eth[i]*100, 2)
        self.ethnicity_pct = {'White': eth[0], 'Black': eth[1], 'Hispanic': eth[2], 'Asian': eth[3],
                              'American Indian/Alaska Native': eth[4], 'Native Hawaiian/Pacific Islander': eth[5],
                              'Multi-Race': eth[6], 'Unknown': eth[7]}

    def set_social_econ_pct(self, data):
        """
        Set Breakdown by Family Income
        :param data: json raw data
        """
        raw_data = [data.get('latest.student.share_lowincome.0_30000'), data.get('latest.student.share_middleincome.30001_48000'),
                    data.get('latest.student.share_middleincome.48001_75000'), data.get('latest.student.share_highincome.75001_110000'),
                    data.get('latest.student.share_highincome.110001plus')]
        for i in range(len(raw_data)):
            if (raw_data[i] is None) or (not isinstance(raw_data[i], int)):
                raw_data[i] = 'Not reported'
            else:
                raw_data[i] = int(raw_data[i]*100)

        self.social_econ_pct = {'Family Income 0-30k': raw_data[0],
                                'Family Income 30k-48k': raw_data[1],
                                'Family Income 48k-75k': raw_data[2],
                                'Family Income 75k-110k': raw_data[3],
                                'Family Income 110k+': raw_data[4]}

    def get_majors(self, data):
        """
        Append List of Major Objects to College
        :param data: json major data
        """
        self.majors = []
        for maj in data:
            if not maj.get('credential').get('level') == 3:
                continue
            mean_debt = maj.get('debt').get('parent_plus').get('all').get('eval_inst').get('average')
            self.majors.append(Major(school=self.name, name=maj.get('title'), mean_debt=mean_debt))

    def set_sports_teams(self, men, women):
        """
        Set sports teams in single string
        :param men: list of men sports
        :param women: list of women sports
        """
        self.sports_teams = {"Men's Sports": ', '.join(men), "Women's Sports": ', '.join(women)}

    def set_outcomes(self, outcome):
        """
        Set employment outcome 6 month after graduation
        :param outcome: list containing percentage employed string
        """
        if len(outcome) < 1:
            self.outcomes = 'Not Reported'
        else:
            self.outcomes = outcome[0] + ' employed 6 months after graduation'

    def set_has_aid(self):
        """
        Check if school offers aid
        """
        for a in self.aid.values():
            if isinstance(a, str):
                if a != 'NA' and a != 'Not reported':
                    self.has_aid = 'Available'
                    return
            elif isinstance(a, dict):
                for b in a.values():
                    if b[-4:] != 'NA, ':
                        self.has_aid = 'Available'
                        return
        self.has_aid = 'Not Available'

    def to_csv_row(self):
        """
        Exports object to list of stringified attributes. List attributes are converted to comma separated string.
        Unimplemented/Depricated attributes are dropped.
        :return: list of college attributes
        """
        row = [vars(self)[x] for x in vars(self) if x != 'majors' and x != 'has_aid']
        row[41] = '\n'.join([x+': '+y for x, y in row[41].items()])
        row[10] = '\n'.join([x+': '+y for x, y in row[10].items()])
        row[35] = '\n'.join([x+': '+y for x, y in row[35].items()])
        row[12] = '\n'.join([x+': $'+str(y) for x, y in row[12].items()])
        aid_keys = list(row[13])
        aid_values = list(row[13].values())
        aid = aid_keys[0]+':\n'+'\n'.join([x+': '+y for x, y in aid_values[0].items()])+'\n\n'
        aid += aid_keys[1]+':\n'+'\n'.join([x+': '+y for x, y in aid_values[1].items()])+'\n\n'
        aid += aid_keys[2]+':\n'+'\n'.join([x+': '+y for x, y in aid_values[2].items()])
        row[13] = aid
        del aid, aid_keys, aid_values
        row[20] = '\n'.join([x+': '+y for x, y in row[20].items()])
        row[29] = '\n'.join([x+': '+str(y)+'%' for x, y in row[29].items()])
        row[30] = '\n'.join([x+': '+str(y)+'%' for x, y in row[30].items()])
        row[32] = '\n'.join([x+': '+str(y)+'%' for x, y in row[32].items()])
        row[40] = '\n'.join([x+': '+y for x, y in row[40].items()])
        return row


class Major:
    """
    Defines a Major.
    """
    def __init__(self, school, name, count=0, mean_debt='NA', career='NA'):
        self.school = school  # associated school
        self.name = name  # name of major
        self.count = count  # number of active students in major
        self.mean_debt = mean_debt  # mean debt of graduates
        self.career = career  # Top career outcomes for major graduates

