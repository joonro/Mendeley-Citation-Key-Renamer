# This Python file uses the following encoding: utf-8
import os
import apsw
import re

from pprint import pprint

def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None

abbr_rule = {'&': '',
             'academy': 'acad',
             'acm': 'acm',
             'acta': 'acta',
             'advances': 'advances',
             'african': 'african',
             'agricultural': 'agr',
             'algorithms': 'algorithm',
             'american': 'am',
             'annual': 'ann',
             'analysis': 'anal',
             'and': '',
             'annals': 'ann',
             'applications': 'appl',
             'applied': 'appl',
             'association': 'assoc',
             'asian': 'asian',
             'banking': 'banking',
             'behavior': 'behav',
             'behavioral': 'behav',
             'bell': 'bell',
             'biometrika': 'biometrika',
             'biomechanics': 'biomech',
             'book': 'book',
             'bulletin': 'bull',
             'business': 'bus',
             'cell': 'cell',
             'clinical': 'clin',
             'control': 'control',
             'credit': 'credit',
             'cognitive': 'cognitive',
             'computational': 'computational',
             'computer': 'comp',
             'computers': 'comp',
             'computing': 'comput',
             'consumer': 'cons',
             'design': 'design',
             'development': 'devel',
             'differential': 'differ',
             'distributed': 'distr',
             'dynamics': 'dynam',
             'ecological': 'ecol',
             'econometrica': 'econometrica',
             'econometrics': 'econometrics',
             'economic': 'econ',
             'economy': 'economy',
             'economica': 'economica',
             'economics': 'econ',
             'economist': 'economist',
             'education': 'educ',
             'educational': 'educ',
             'electronic': 'electron',
             'electromagnetics': 'electrom',
             'empirical': 'empirical',
             'engineering': 'eng',
             'energy': 'energy',
             'environment': 'environ',
             'environmental': 'environ',
             'ergonomics': 'ergonomics',
             'evolutionary': 'evol',
             'european': 'europ',
             'experimental': 'exper',
             'factors': 'fact',
             'federal': 'fed',
             'finance': 'finance',
             'financial': 'finan',
             'for': '',
             'game': 'game',
             'games': 'game',
             'global': 'global',
             'handbook': 'handbook',
             'health': 'health',
             'high': 'high',
             'history': 'hist',
             'human': 'human',
             'in': '',
             'industrial': 'ind',
             'information': 'info',
             'interactive': 'interact',
             'international': 'int',
             'inquiry': 'inquiry',
             'journal': 'j',
             'labor': 'lab',
             'law': 'law',
             'letters': 'letters',
             'literature': 'lit',
             'marketing': 'market',
             'macroeconomics': 'macroecon',
             'management': 'manage',
             'manual': 'manual',
             'manuscript': 'manuscript',
             'mathematical': 'math',
             'mathematics': 'mathematics',
             'methods': 'methods',
             'money': 'money',
             'monetary': 'monetary',
             'multivariate': 'multivar',
             'nature': 'nature',
             'nber': 'nber',
             'new': 'new',
             'numerical': 'numer',
             'numerica': 'umerica',
             'of': '',
             'on': '',
             'organization': 'organ',
             'operations': 'operations',
             'optimization': 'optim',
             'paper': 'paper',
             'parallel': 'parallel',
             'parallel': 'parallel',
             'performance': 'perform',
             'personality': 'pers',
             'perspectives': 'perspect',
             'physics': 'phys',
             'policy': 'pol',
             'political': 'polit',
             'practice': 'pract',
             'prevention': 'prevent',
             'proceedings': 'proceed',
             'psychology': 'psychol',
             'psychological': 'psychol',
             'psychologist': 'psychol',
             'python': 'python',
             'public': 'public',
             'quantitative': 'quant',
             'quarterly': 'quart',
             'rand': 'rand',
             'religion': 'relig',
             'research': 'res',
             'review': 'rev',
             'retailing': 'retailing',
             'risk': 'risk',
             'royal': 'roy',
             'science': 'sci',
             'scientific': 'sci',
             'services': 'serv',
             'siam': 'siam',
             'simulation': 'sim',
             'sinica': 'sinica',
             'society': 'society',
             'social': 'soc',
             'sociology': 'sociol',
             'software': 'softw',
             'sport': 'sport',
             'sports': 'sport',
             'ssrn': 'ssrn',
             'strategy': 'strategy',
             'strategic': 'strategic',
             'statistica': 'stat',
             'statistical': 'statistical',
             'statistics': 'statist',
             'statistician': 'statistician',
             'studies': 'stud',
             'study': 'study',
             'the': '',
             'theoretical': 'theoretical',
             'theory': 'theory',
             'university': 'univ',
             'working': 'working',
             'world': 'world',
             'york': 'york',
             }

unicode_rule = {'. ': '-',
                ' ': '-',
                '.': '',
                "'": '',
                u'å': 'a',
                u'ä': 'a',
                u'é': 'e',
                u'è': 'e',
                u'í': 'i',
                u'ö': 'o',
                u'ø': 'o',
                u'ç': 'c',
                u'ü': 'u',
                u'\u2026': '...',
                }

def remove_unicode(arg):
    for a_unicode in unicode_rule.keys():
        arg = arg.replace(a_unicode, unicode_rule[a_unicode])
    return(arg)

if __name__ == '__main__':
    '''
    change Mendeley citation key to author-author-year-journalabbr format
    '''
    sqlite = 'joonhyoung.ro@gmail.com@www.mendeley.com.sqlite'  # change

    if os.name == 'nt':
        path_db = r'\home\joon\AppData\Local\Mendeley Ltd\Mendeley Desktop\{}'.format(sqlite)
    else:
        path_db = '/home/joon/.local/share/data/Mendeley Ltd./Mendeley Desktop/'.format(sqlite)

    con = apsw.Connection(path_db)

    con.createscalarfunction("REGEXP", regexp)

    cur = con.cursor()

    # remove C:/ from localUrl
    cur.execute("SELECT localUrl FROM Files WHERE localUrl LIKE '%file:///C:/home%';")
    localUrls = cur.fetchall()[:]
    if len(localUrls):
        cur.execute(("UPDATE Files SET localUrl = REPLACE(localUrl, 'file:///C:/home',"
                     "'file:///home') WHERE localUrl LIKE '%file:///C:/home%';"))

        print('Fixed the following localUrl(s):')
        pprint(localUrls)

    cur.execute("SELECT id FROM Documents")
    documentids = cur.fetchall()[:]

    modified = []  # list of modified citations
    errors = []  # list of citations with errors

    for i, k in enumerate(documentids):
        docid = k[0]
        cur.execute(("SELECT publication FROM Documents WHERE "
                     "id='{}'").format(docid))

        publication = cur.fetchall()[:][0][0]

        if not publication:
            continue

        # get the journal abbr
        exception = False
        key_publication = ''
        for j, word in enumerate(publication.split(' ')):
            word = word.replace('.', '')
            word = word.replace(',', '')
            word = word.replace(':', '')
            try:
                temp_abbr = abbr_rule[word.lower()]
            except:
                print((u'no word: "{}" in {}'
                       '').format(remove_unicode(word),
                           remove_unicode(publication)))
                exception = True
                continue

            if len(temp_abbr):
                key_publication += abbr_rule[word.lower()] + '-'

        if exception:
            continue

        key_publication = key_publication[:-1]

        cur.execute(("SELECT lastName FROM DocumentContributors WHERE "
                     "documentID='{}'").format(docid))

        lastnames = cur.fetchall()[:]

        key_author = ''
        for j, lastname in enumerate(lastnames):
            if j == 3:
                key_author += ' ' + 'et-al'
                break
            else:
                key_author += ' ' + lastname[0]

        key_author = key_author.strip().lower()

        key_author = remove_unicode(key_author)
        key_publication = remove_unicode(key_publication)

        cur.execute(("SELECT year FROM Documents WHERE "
                     "id='{}'").format(docid))

        year = cur.fetchall()[:][0][0]

        citationkey = '{}-{}-{}'.format(key_author, year, key_publication)

        cur.execute(("SELECT citationKey FROM Documents WHERE "
                     "id='{}'").format(docid))

        citationkey_old = cur.fetchall()[:][0][0]

        if citationkey != citationkey_old:
            if not 'test-run':
                if citationkey_old:
                    modified.append(citationkey_old + ' -> ' +  citationkey)
                else:
                    modified.append('" " -> ' +  citationkey)
            else:
                try:
                    cur.execute(("UPDATE Documents SET citationKey="
                                "'{new}' WHERE ID={ID}").format(new=citationkey,
                                                                ID=docid))
                    modified.append(citationkey_old + ' -> ' + citationkey)
                except:
                    errors.append('error: ' + citationkey)

    from pprint import pprint
    pprint(modified)
    pprint(errors)


if not 'obsolete':
    if re.search(r'([a-z]+)(\d+)', k[0], re.UNICODE|re.IGNORECASE):
        new = re.sub(r'([a-z]+)(\d+).+', r'\1-\2', k[0], re.UNICODE, re.IGNORECASE)

        try:
            new += '-' + journal_abbr[publications[i][0]]
            new = new.lower()
            new = new.replace('. ', '-')
            new = new.replace(' ', '-')
            new = new.replace('.', '')

            cur.execute(("UPDATE {table} SET citationKey='{new}' WHERE ID={ID}"
                        ).format(table=table, new=new, ID=docid))

            print('{old} -> {new}'.format(old=k[0], new=new))

        except:
            print(k[0])

    else:
        print(k[0])


    for i, k in enumerate(citationkeys):
        if k[0]:
            if re.search(r'\d+[a-z]+', k[0], re.UNICODE|re.IGNORECASE):
                new = re.sub(r'(\d+)[a-z]+', r'\1', k[0], re.UNICODE, re.IGNORECASE)
                try:
                    new += '-' + journal_abbr[publications[i][0]]
                    new = new.lower()
                    new = new.replace('. ', '-')
                    new = new.replace(' ', '-')
                    new = new.replace('.', '')

                    cur.execute("UPDATE {table} SET citationKey='{new}' WHERE ID={ID}".format(table=table, new=new, ID=docid))

                    print('{old} -> {new}'.format(old=k[0], new=new) )

                except:
                    print(k[0])

            else:
                print(k[0])

    # duplicated journal names
    for i, k in enumerate(citationkeys):

        if k[0]:

            try:
                new = journal_abbr[publications[i][0]] + ' ' + journal_abbr[publications[i][0]]
                new = new.lower()
                new = new.replace('. ', '-')
                new = new.replace(' ', '-')
                new = new.replace('.', '')

                if k[0].find(new) != -1:
                    new = k[0][:-len(new)/2]

                    cur.execute("UPDATE {table} SET citationKey='{new}' WHERE ID={ID}".format(table=table, new=new, ID=docid))

                    print('{old} -> {new}'.format(old=k[0], new=new) )

            except:
                print(k[0])


    cur.execute("SELECT tag from DocumentTags where tag REGEXP 'class-[0-9]'")
    cur.execute("SELECT citationKey FROM Documents WHERE citationKey REGEXP {}".format(r'[A-Z][a-z]+[0-9]+', ))

    cur.execute("SELECT citationKey FROM Documents WHERE citationKey REGEXP {}".format('W[a-z]+1995',))

    cur.execute("SELECT tag from DocumentTags where tag like '%Class%'")
    pprint(cur.fetchall())

    cur.execute("UPDATE DocumentTags set tag={} where tag={}".format('class-9', 'Class_9'))
    cur.execute("SELECT tag from DocumentTags where tag like '%Class%'")

    cur.execute("SELECT citationKey from Documents")
    pprint(cur.fetchall())
