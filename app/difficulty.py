###########################################################################
# Copyright 2019 (C) Hui Lan <hui.lan@cantab.net>
# Written permission must be obtained from the author for commercial uses.
###########################################################################

# Purpose: compute difficulty level of a English text

import pickle
import math
from wordfreqCMD import remove_punctuation, freq, sort_in_descending_order, sort_in_ascending_order


def load_record(pickle_fname):
    f = open(pickle_fname, 'rb')
    d = pickle.load(f)
    f.close()
    return d


def difficulty_level_from_frequency(word, d):
    level = 1
    if not word in d:
        return level
    
    if 'what' in d:
        ratio = (d['what']+1)/(d[word]+1) # what is a frequent word
        level = math.log( max(ratio, 1), 2)

    level = min(level, 8) 
    return level


def get_difficulty_level(d1, d2):
    d = {}
    L = list(d1.keys())  # in d1, we have freuqence for each word
    L2 = list(d2.keys()) # in d2, we have test types (e.g., CET4,CET6,BBC) for each word
    L.extend(L2)
    L3 = list(set(L)) # L3 contains all words
    for k in L3:
        if k in d2:
            if 'CET4' in d2[k]:
                d[k] = 4 # CET4 word has level 4
            elif 'CET6' in d2[k]:
                d[k] = 6
            elif 'BBC' in d2[k]:
                d[k] = 8
                if k in d1: # BBC could contain easy words that are not in CET4 or CET6.  So 4 is not reasonable.  Recompute difficulty level.
                    d[k] = min(difficulty_level_from_frequency(k, d1), d[k])
        elif k in d1:
            d[k] = difficulty_level_from_frequency(k, d1)

    return d

        

def revert_dict(d):
    '''
    In d, word is the key, and value is a list of dates.
    In d2 (the returned value of this function), time is the key, and the value is a list of words picked at that time.
    '''
    d2 = {}
    for k in d:
        if type(d[k]) is list:  # d[k] is a list of dates.
            lst = d[k]
        elif type(d[k]) is int: # for backward compatibility.  d was sth like {'word':1}.  The value d[k] is not a list of dates, but a number representing how frequent this word had been added to the new word book. 
            freq = d[k]
            lst = freq*['2021082019'] # why choose this date?  No particular reasons.  I fix the bug in this date.

        for time_info in lst:
            date = time_info[:10] # until hour
            if not date in d2:
                d2[date] = [k]
            else:
                d2[date].append(k)
    return d2


def user_difficulty_level(d_user, d):
    d_user2 = revert_dict(d_user) # key is date, and value is a list of words added in that date
    count = 0
    geometric = 1
    for date in sorted(d_user2.keys(), reverse=True): # most recently added words are more important while determining user's level
        lst = d_user2[date] # a list of words
        lst2 = [] # a list of tuples, (word, difficulty level)
        for  word in lst:
            if word in d:
                lst2.append((word, d[word]))

        lst3 = sort_in_ascending_order(lst2) # easiest tuple first
        #print(lst3)
        for t in lst3:
            word = t[0]
            hard = t[1]
            #print('WORD %s HARD %4.2f' % (word, hard))
            geometric = geometric * (hard)
            count += 1
            if count >= 10:
                return geometric**(1/count)

    return geometric**(1/max(count,1))


def text_difficulty_level(s, d):
    s = remove_punctuation(s)
    L = freq(s)

    lst = [] # a list of tuples, each tuple being (word, difficulty level)
    for x in L:
        word = x[0]
        if word in d:
            lst.append((word, d[word]))

    lst2 = sort_in_descending_order(lst) # most difficult words on top
    #print(lst2)
    count = 0
    geometric = 1
    for t in lst2:
        word = t[0]
        hard = t[1]
        geometric = geometric * (hard)
        count += 1
        if count >= 20: # we look for n most difficult words
            return geometric**(1/count)
        
    return geometric**(1/max(count,1))



if __name__ == '__main__':


    d1 = load_record('frequency.p')
    #print(d1)

    d2 = load_record('words_and_tests.p')
    #print(d2)


    d3 = get_difficulty_level(d1, d2)

    s = '''
South Lawn
11:53 A.M. EDT
THE PRESIDENT:  Hi, everybody.  Hi.  How are you?  So, the stock market is doing very well.
The economy is booming.  We have a new record in sight.  It could happen even today.
But we have a new stock market record.  I think it’ll be about 118 times that we’ve broken the record.
Jobs look phenomenal.
    '''
    s = '''
By the authority vested in me as President by the Constitution and the laws of the United States, after carefully considering the reports submitted to the Congress by the Energy Information Administration, including the report submitted in October 2019, and other relevant factors, including global economic conditions, increased oil production by certain countries, the global level of spare petroleum production capacity, and the availability of strategic reserves, I determine, pursuant to section 1245(d)(4)(B) and (C) of the National Defense Authorization Act for Fiscal Year 2012, Public Law 112-81, and consistent with prior determinations, that there is a sufficient supply of petroleum and petroleum products from countries other than Iran to permit a significant reduction in the volume of petroleum and petroleum products purchased from Iran by or through foreign financial institutions.

'''

    s = '''
Democrats keep their witnesses locked behind secure doors, then flood the press with carefully sculpted leaks and accusations, driving the Trump-corruption narrative. And so the party goes, galloping toward an impeachment vote that would overturn the will of the American voters—on a case built in secret.

Conservative commentators keep noting that Mrs. Pelosi’s refusal to hold a vote on the House floor to authorize an official impeachment inquiry helps her caucus’s vulnerable members evade accountability. But there’s a more practical and uglier reason for Democrats to skip the formalities. Normally an authorization vote would be followed by official rules on how the inquiry would proceed. Under today’s process, Mr. Schiff gets to make up the rules as he goes along. Behold the Lord High Impeacher.

Democrats view control over the narrative as essential, having learned from their Russia-collusion escapade the perils of transparency. They banked on special counsel Robert Mueller’s investigation proving impeachment fodder, but got truth-bombed. Their subsequent open hearings on the subject—featuring Michael Cohen, Mr. Mueller and Corey Lewandowski —were, for the Democrats, embarrassing spectacles, at which Republicans punched gaping holes in their story line.

Mr. Schiff is making sure that doesn’t happen again; he’ll present the story, on his terms. His rules mean he can issue that controlling decree about “only one” transcript and Democratic staff supervision of Republican members. It means he can bar the public, the press and even fellow representatives from hearings, even though they’re unclassified.
'''

    s = '''
Unemployment today is at a 50-year low.  There are more Americans working today than ever before.  Median household income in the last two and half years has risen by more than $5,000.  And that doesn’t even account for the savings from the President’s tax cuts or energy reforms for working families.

Because of the President’s policies, America has added trillions of dollars of wealth to our economy while China’s economy continues to fall behind.

To level the playing field for the American worker against unethical trade practices, President Trump levied tariffs on $250 billion in Chinese goods in 2018.  And earlier this year, the President announced we would place tariffs on another $300 billion of Chinese goods if significant issues in our trading relationship were not resolved by December of this year.
'''
    s = '''
Needless to say, we see it very differently.  Despite the great power competition that is underway, and America’s growing strength, we want better for China.  That’s why, for the first time in decades, under President Donald Trump’s leadership, the United States is treating China’s leaders exactly how the leaders of any great world power should be treated — with respect, yes, but also with consistency and candor.
'''
    s = '''
Brexit is the scheduled withdrawal of the United Kingdom from the European Union. Following a June 2016 referendum, in which 51.9% voted to leave, the UK government formally announced the country's withdrawal in March 2017, starting a two-year process that was due to conclude with the UK withdrawing on 29 March 2019. As the UK parliament thrice voted against the negotiated withdrawal agreement, that deadline has been extended twice, and is currently 31 October 2019. The Benn Act, passed in September 2019, requires the government to seek a third extension.
'''

    s = '''
The argument for Brexit
According to the BBC, the push to leave the EU was advocated mostly by the UK Independence Party and was not supported by the Prime Minister, David Cameron. Members of the UK Independence Party argued that Britain’s participation in the EU was a restrictive element for the country.

As one of the EU’s primary initiatives is free movement within the region the party’s main arguments centered around regaining border control and reclaiming business rights. In addition, supporters of Brexit cited the high EU membership fees as a negative aspect of participation in the EU. It was argued that if the UK separates itself from the EU, these fees can be used to benefit the UK.

The argument against Brexit
The Conservative Party and the Prime Minister were strongly in favor of remaining with the EU. As a result of the decision to discontinue its participation in the EU, the Prime Minister has made a public statement that he will be relinquishing his position. He believes that the country needs a leader with the same goals as the majority of the country. He has promised a new PM will be in place by early September.

The argument against Brexit pertains mostly to the business benefits. The argument is that the UK receives business benefits by being able to participate in the single market system established by the EU. In response to the criticism against the open borders, proponents believe that the influx of immigrants helps develop an eager workforce and fuels public service projects.

Leaders in favor of staying also worry about the political backlash that could possibly result from other countries who favored staying with the EU. In addition, proponents of remaining with the EU believe that being part of a wider community of nations provides economic and cultural strength, as well as an additional element of security.

What does Brexit mean for the future?
While the decision marked a huge statement for the UK, the referendum vote is not legally binding. There are still many hurdles that must be dealt with before Brexit can become a reality.

The UK is still subject to the laws of the EU until Britain’s exit becomes legal. In order for the UK to make its break official, the country needs to invoke Article 50. It is unclear exactly what this process will entail or how long it will take as Britain is the first country to take its leave of the EU. Once Article 50 has been formally invoked, the UK has two years to negotiate its departure with the other member states. But according to the BBC, “Extricating the UK from the EU will be extremely complex, and the process could drag on longer than that.”

Amidst the aftermath of this shocking referendum vote, there is great uncertainty as political leaders decide what this means for the UK.

'''


    s = '''
British Prime Minister Boris Johnson walks towards a voting station during the Brexit referendum in Britain, June 23, 2016. (Photo: EPA-EFE)

LONDON – British Prime Minister Boris Johnson said Thursday he will likely ask Parliament to approve an election as part of an effort to break a Brexit deadlock.

It is not clear if the vote, which Johnson wants to hold on Dec. 12, will take place as opposition lawmakers must also back the move.

They are expected to vote on the measure on Monday. 

Johnson's announcement comes ahead of an expected decision Friday from the European Union over whether to delay Britain's exit from the bloc for three months. 

Britain's leader has been steadfastly opposed to any extension to the nation's scheduled Oct. 31 departure date from the EU, although in a letter to the leader of the opposition Labour Party this week he said he would accept a short technical postponement, "say to 15 or 30 November," to allow lawmakers to implement an EU withdrawal bill. 

Johnson's decision to offer to call an election follows lawmakers' rejection of his plan to rush through an EU exit bill that runs to hundreds of pages in just three days. They want more time to scrutinize the legislation and to make sure it does not leave the door open to a possible "no-deal" Brexit during future exit negotiations with the EU that will run through next year. A "no-deal" Brexit could dramatically harm Britain's economy. 

The prime minister was forced to ask for an extension to Britain's EU departure date after Britain's Parliament passed a law to ward off the threat of a "no-deal" Brexit.

Johnson has repeatedly pledged to finalize the first stage, a transition deal, of Britain's EU divorce battle by Oct. 31. A second stage will involve negotiating its future relationship with the EU on trade, security and other salient issues.
'''


    s = '''
Thank you very much. We have a Cabinet meeting. We’ll have a few questions after grace. And, if you would, Ben, please do the honors.

THE PRESIDENT: All right, thank you, Ben. That was a great job. Appreciate it.

The economy is doing fantastically well. It’s getting very close to another record. We’ve had many records since we won office. We’re getting very close to another record. I don’t know if anybody saw it: The household median income for eight years of President Bush, it rose $400. For eight years of President Obama, it rose $975. And for two and half years of President Trump — they have it down as two and a half years — it rose $5,000, not including $2,000 for taxes. So it rose, let’s say, $7,000. So in two and a half years, we’re up $7,000, compared to $1,000, compared to $400. And that’s for eight years and eight years.

That’s a number that just came out, but that’s a number that I don’t know how there could be any dispute or any — I’ve never heard a number like that, meaning the economy is doing fantastically well.

We need — for our farmers, our manufacturers, for, frankly, unions and non-unions, we need USMCA to be voted on. If it’s voted on, it’ll pass. It’s up to Nancy Pelosi to put it up. If she puts it up, it’s going to pass. It’s going to be very bipartisan. It’s something that’s very much needed. It’ll be hundreds of thousands of jobs.


'''




    #f = open('bbc-fulltext/bbc/entertainment/001.txt')
    f = open('wordlist.txt')
    s = f.read()
    f.close()



    
    print(text_difficulty_level(s, d3))

            
