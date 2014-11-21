# This Python file uses the following encoding: utf-8
import os
import apsw
import re

from pprint import pprint
from titlecase import titlecase

from abbr_rule import abbr_rule

def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None

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
                u'Ö': 'o',
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
        path_db = r'\Users\joon\AppData\Local\Mendeley Ltd\Mendeley Desktop\{}'.format(sqlite)
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
        cur.execute(("SELECT Publication FROM Documents WHERE "
                     "id='{}'").format(docid))

        publication = cur.fetchall()[:][0][0]

        if publication:
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
                    key_publication += abbr_rule[word.lower()].title() + '_'

            key_publication = key_publication[:-1]

            if exception:
                continue
        else:
            cur.execute(("SELECT Type FROM Documents WHERE "
                         "id='{}'").format(docid))
            item_type = cur.fetchall()[:][0][0]
            if item_type == "Book":
                key_publication = "book"

        cur.execute(("SELECT lastName FROM DocumentContributors WHERE "
                     "documentID='{}'").format(docid))

        lastnames = cur.fetchall()[:]

        key_author = ''
        for j, lastname in enumerate(lastnames):
            if j == 3:
                key_author += '_' + 'et-al'
                break
            else:
                key_author += '_' + lastname[0]

        key_author = key_author.strip()[1:]

        key_author = remove_unicode(key_author)
        key_publication = remove_unicode(key_publication)

        cur.execute(("SELECT year FROM Documents WHERE "
                     "id='{}'").format(docid))

        year = cur.fetchall()[:][0][0]

        citationkey = '{}_{}_{}'.format(key_author, year, key_publication)

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

        # titlecase(title)
        cur.execute(("SELECT Title FROM Documents WHERE "
                     "id='{}'").format(docid))

        title = cur.fetchall()[:][0][0]
        titlecased = titlecase(title)

        if title != titlecased:
            newtitle = titlecased.replace("'", "''")

            try:
                cur.execute(("UPDATE Documents SET Title="
                    "'{title}' WHERE ID={ID}").format(title=newtitle, ID=docid))
                modified.append(title + ' -> ' + titlecased)
            except:
                errors.append('error: ' + title)

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

