from User import *
app = Flask(__name__)
app.secret_key = 'lunch.time!'

path_prefix = '/var/www/wordfreq/wordfreq/'
path_prefix = './'  # comment this line in deployment
class Function:
    def get_random_image(path):
        img_path = random.choice(glob.glob(os.path.join(path, '*.jpg')))
        return img_path[img_path.rfind('/static'):]


    def get_random_ads():
        ads = random.choice(['个性化分析精准提升', '你的专有单词本', '智能捕捉阅读弱点，针对性提高你的阅读水平'])
        return ads + '。'


    def within_range(x, y, r):
        return x > y and abs(x - y) <= r


    def load_freq_history(path):
        d = {}
        if os.path.exists(path):
            d = pickle_idea.load_record(path)
        return d


    def get_today_article(user_word_list, articleID):
        rq = RecordQuery(path_prefix + 'static/wordfreqapp.db')
        if articleID == None:
            rq.instructions("SELECT * FROM article")
        else:
            rq.instructions('SELECT * FROM article WHERE article_id=%d' % (articleID))
        rq.do()
        result = rq.get_results()

        # Choose article according to reader's level
        d1 = Function.load_freq_history(path_prefix + 'static/frequency/frequency.p')
        d2 = Function.load_freq_history(path_prefix + 'static/words_and_tests.p')
        d3 = get_difficulty_level(d1, d2)

        d = {}
        d_user = Function.load_freq_history(user_word_list)
        user_level = user_difficulty_level(d_user,
                                           d3)  # more consideration as user's behaviour is dynamic. Time factor should be considered.
        random.shuffle(result)  # shuffle list
        d = random.choice(result)
        text_level = text_difficulty_level(d['text'], d3)
        if articleID == None:
            for reading in result:
                text_level = text_difficulty_level(reading['text'], d3)
                # print('TEXT_LEVEL %4.2f' % (text_level))
                if Function.within_range(text_level, user_level, 0.5):
                    d = reading
                    break

        s = '<p><i>According to your word list, your level is <b>%4.2f</b> and we have chosen an article with a difficulty level of <b>%4.2f</b> for you.</i></p>' % (
            user_level, text_level)
        s += '<p><b>%s</b></p>' % (d['date'])
        s += '<p><font size=+2>%s</font></p>' % (d['text'])
        s += '<p><i>%s</i></p>' % (d['source'])
        s += '<p><b>%s</b></p>' % (Function.get_question_part(d['question']))
        s = s.replace('\n', '<br/>')
        s += '%s' % (Function.get_answer_part(d['question']))
        session['articleID'] = d['article_id']
        return s


    def appears_in_test(word, d):
        if not word in d:
            return ''
        else:
            return ','.join(d[word])


    def get_time():
        return datetime.now().strftime('%Y%m%d%H%M')  # upper to minutes


    def get_question_part(s):
        s = s.strip()
        result = []
        flag = 0
        for line in s.split('\n'):
            line = line.strip()
            if line == 'QUESTION':
                result.append(line)
                flag = 1
            elif line == 'ANSWER':
                flag = 0
            elif flag == 1:
                result.append(line)
        return '\n'.join(result)


    def get_answer_part(s):
        s = s.strip()
        result = []
        flag = 0
        for line in s.split('\n'):
            line = line.strip()
            if line == 'ANSWER':
                flag = 1
            elif flag == 1:
                result.append(line)
        # https://css-tricks.com/snippets/javascript/showhide-element/
        js = '''
    <script type="text/javascript">
        function toggle_visibility(id) {
           var e = document.getElementById(id);
           if(e.style.display == 'block')
              e.style.display = 'none';
           else
              e.style.display = 'block';
        }
    </script>   
        '''
        html_code = js
        html_code += '\n'
        html_code += '<button onclick="toggle_visibility(\'answer\');">ANSWER</button>\n'
        html_code += '<div id="answer" style="display:none;">%s</div>\n' % ('\n'.join(result))
        return html_code