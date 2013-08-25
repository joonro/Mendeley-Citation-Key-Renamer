# This Python file uses the following encoding: utf-8
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
             'applied': 'appl',
             'association': 'assoc',
             'asian': 'asian',
             'banking': 'banking',
             'behavior': 'behav',
             'biometrika': 'biometrika',
             'biomechanics': 'biomech',
             'bulletin': 'bull',
             'business': 'bus',
             'cell': 'cell',
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
             'dynamics': 'dynam',
             'econometrica': 'econometrica',
             'econometrics': 'econometrics',
             'economic': 'econ',
             'economy': 'economy',
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
             'european': 'europ',
             'experimental': 'exper',
             'factors': 'fact',
             'federal': 'fed',
             'finance': 'finance',
             'financial': 'finan',
             'for': '',
             'handbook': 'handbook',
             'health': 'health',
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
             'performance': 'perform',
             'personality': 'pers',
             'perspectives': 'perspect',
             'policy': 'pol',
             'political': 'polit',
             'practice': 'pract',
             'prevention': 'prevent',
             'proceedings': 'proceed',
             'psychology': 'psychol',
             'psychological': 'psychol',
             'psychologist': 'psychol',
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
             'sinica': 'sinica',
             'society': 'society',
             'social': 'soc',
             'sociology': 'sociol',
             'software': 'softw',
             'ssrn': 'ssrn',
             'strategy': 'strategy',
             'strategic': 'strategic',
             'statistica': 'stat',
             'statistical': 'statistical',
             'statistics': 'statist',
             'statistician': 'statistician',
             'studies': 'stud',
             'the': '',
             'theoretical': 'theoretical',
             'theory': 'theory',
             'university': 'univ',
             'working': 'working',
             'york': 'york',
             }

unicode_rule = {'. ': '-',
                ' ': '-',
                '.': '',
                "'": '',
                u'??': 'a',
                u'??': 'e',
                u'??': 'e',
                u'??': 'o',
                u'??': 'o',
                u'??': 'c',
                u'??': 'u',
                }

def remove_unicode(arg):
    for a_unicode in unicode_rule.keys():
      arg = arg.replace(a_unicode, unicode_rule[a_unicode])
    return(arg)

if __name__ == '__main__':
    '''
    change Mendeley citation key to author-author-year-journalabbr format
    '''

    # load journal abbr data
    with open('/home/joon/Dropbox/python/journal-abbr.txt', 'rb') as f:
        journal_abbr = {line.strip().split(': ')[0].lower(): line.strip().split(': ')[1].lower()  for line in f}

    con = apsw.Connection('/home/joon/.local/share/data/Mendeley Ltd./Mendeley Desktop/joonhyoung.ro@gmail.com@www.mendeley.com.sqlite')

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

    cur.execute("SELECT citationKey FROM Documents")
    citationkeys = cur.fetchall()[:]

    cur.execute("SELECT publication FROM Documents")
    publications = cur.fetchall()[:]

    cur.execute("SELECT id FROM Documents")
    documentids = cur.fetchall()[:]

    cur.execute("SELECT year FROM Documents")
    years = cur.fetchall()[:]

    modified = []  # list of modified citations
    errors = []  # list of citations with errors

    for i, k in enumerate(publications):
        if not k[0]:
            continue

        publication = k[0]

        if publication[:3] == 'The ':
            publication = publication[4:]

        if journal_abbr.has_key(publication.lower()):
            citation_journal = journal_abbr[publication.lower()]

            cur.execute(("SELECT lastName FROM DocumentContributors WHERE "
                         "documentID = '{}'").format(documentids[i][0]))

            lastnames = cur.fetchall()[:]

            citation_author = ''
            for j, lastname in enumerate(lastnames):
                if j == 3:
                    citation_author += ' ' + 'et-al'
                    break
                else:
                    citation_author += ' ' + lastname[0]

            citation = citation_author.strip() + '-' + str(years[i][0]) + '-' + citation_journal

            citation = citation.lower()
            citation = citation.replace('. ', '-')
            citation = citation.replace(' ', '-')
            citation = citation.replace('.', '')
            citation = citation.replace("'", '')
            citation = citation.replace(u'ä', 'a')
            citation = citation.replace(u'é', 'e')
            citation = citation.replace(u'ö', 'o')
            citation = citation.replace(u'ø', 'o')
            citation = citation.replace(u'ç', 'c')
            citation = citation.replace(u'ü', 'u')

            if citation != citationkeys[i][0]:
                if not 'test-run':
                    if citationkeys[i][0]:
                        modified.append(citationkeys[i][0] + ' -> ' +  citation)

                    else:
                        modified.append('" " -> ' +  citation)

                else:
                    try:
                        cur.execute(("UPDATE Documents SET citationKey = "
                                    "'{new}' WHERE ID = {ID}").format(new=citation,
                                                                      ID=documentids[i][0]))
                        modified.append(citationkeys[i][0] + ' -> ' + citation)
                    except:
                        #import IPython
                        #IPython.embed(); sys.exit()

                        errors.append('error: ' + citation)

        else:
            print(('no publication abbr: {}, documentid: {}'
                   '').format(publication, documentids[i][0]))

    from pprint import pprint
    pprint(modified)
    pprint(errors)


if not 'other stuff':

    if re.search(r'([a-z]+)(\d+)', k[0], re.UNICODE|re.IGNORECASE):
        new = re.sub(r'([a-z]+)(\d+).+', r'\1-\2', k[0], re.UNICODE, re.IGNORECASE)

        try:
            new += '-' + journal_abbr[publications[i][0]]
            new = new.lower()
            new = new.replace('. ', '-')
            new = new.replace(' ', '-')
            new = new.replace('.', '')

            cur.execute("UPDATE {table} SET citationKey = '{new}' WHERE ID = {ID}".format(table = table, new = new, ID = documentids[i][0]))

            print('{old} -> {new}'.format(old = k[0], new = new) )

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

                    cur.execute("UPDATE {table} SET citationKey = '{new}' WHERE ID = {ID}".format(table = table, new = new, ID = documentids[i][0]))

                    print('{old} -> {new}'.format(old = k[0], new = new) )

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

                    cur.execute("UPDATE {table} SET citationKey = '{new}' WHERE ID = {ID}".format(table = table, new = new, ID = documentids[i][0]))

                    print('{old} -> {new}'.format(old = k[0], new = new) )

            except:
                print(k[0])


    cur.execute("SELECT tag from DocumentTags where tag REGEXP 'class-[0-9]'")
    cur.execute("SELECT citationKey FROM Documents WHERE citationKey REGEXP ?", (r'[A-Z][a-z]+[0-9]+', ))

    cur.execute("SELECT citationKey FROM Documents WHERE citationKey REGEXP ?", ('W[a-z]+1995',))

    cur.execute("SELECT tag from DocumentTags where tag like '%Class%'")
    pprint(cur.fetchall())

    cur.execute("UPDATE DocumentTags set tag = ? where tag = ?", ('class-9', 'Class_9'))
    cur.execute("SELECT tag from DocumentTags where tag like '%Class%'")

    cur.execute("SELECT citationKey from Documents")
    pprint(cur.fetchall())
