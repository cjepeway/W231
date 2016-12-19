# datascience@berkeley W231 - Behind the Data: Humans and Values

So, I want to talk up this class in [the MIDS program at Berkeley](https://datascience.berkeley.edu),
_Behind the Data: Humans and Values_, aka _Ethics_.

This is my last semester in MIDS.  Indeed, this is the last day I'll do work for the program,
'cause, see, I'm done.  I graduate here in but days.

But, y'all need to know a bit about what I've been up to.
In particular, y'all need to know about _Ethics_ and the
project I've been working on for lo these past few weeks.

First, our instructors.  They're phenomenal:
* Anna Laruen Hoffman, who really had us going gangbusters when she guested a class
* Deirdre Mulligan, whose intellect, high expectations of her students, and ability to tweeze deep thought out of busy distance learners are all much appreciated
* Nathan Good, his topic mastery and laidback herding of cats make a 9:30PM EST class start nearly a joy

Really, though, the topic is something else.  It's the ethics of data: privacy, governance, furthering human endeavor using it.
And it's unlike any other MIDS class, perhaps save RDADA.
You get to *think* in this class.  Deeply, shallowly, broadly, narrowly.
And you're encouraged to do it.

Why?

So you get your head around how to do right by people
once you're out in the big room, practicing the data science
you've drilled into your head in this very, very challenging program.

"Doing right by people?"  With...data science?
Oh, yes, indeed.

'Cause you can dang sure do wrong by them with it.
You can fill your days with implementing
machine learning pipelines without
thought to whose data you're training on,
or how your models might be used, or
[what happens when you accurately predict
an event folk might rather like to discover
in their own sweet time](http://www.forbes.com/sites/kashmirhill/2012/02/16/how-target-figured-out-a-teen-girl-was-pregnant-before-her-father-did/).  You might mis-classify transactions as
anomalous because of your cohort-bias,
or perhaps not training image recognizers
on all the shades of human skin.

Or you might share microdata
(data that can be tied to an individual)
about customer transactions
on the web, believing it to be
de-identified and so can't be linked
back to real, live human.

Netflix did that, back in the day,
when they offerred
[a million dollar prize](https://netflixprize.com) for help with
recommending DVDs to their subscribers.

They were wrong about the de-identification thing,
and [they got sued & settled out of court](http://www.forbes.com/sites/firewall/2010/03/12/netflix-settles-privacy-suit-cancels-netflix-prize-two-sequel/)
when two researchers,
[Narayanan](https://freedom-to-tinker.com/author/randomwalker/)
and
[Shmatikov](https://www.cs.cornell.edu/~shmat/)
published a way to use
public IMDB ratings
and the Netflix transactions
to determine who watched what movies
in the privacy of their own homes.
Netflix customers were none too happy
that data containing 10% or more of their
private queues were out there
for anyone to tie back to their public face.

Now, Narayanan and Shmatikov
were responsible, mind you: no public disclosures of whether I watch Bambi movies in the wee hours of the night, eg.
But their paper did lead to the shutdown of further Netflix Prizes,
and it kinda sounded a death knell for "collaborative filtering."

It, along with a class visit from
[Khaled El Emam](https://www.privacy-analytics.com/team/khaled-el-emam/)
got me interested in replicating the Netflix Prize Killers work.

So that turned into my course project.

You can see [the presentation I gave on it](https://github.com/cjepeway/W231-Public-Advocacy/blob/master/OtTotNPK.pdf), if you like.
I had fun working on it, and my classmates seemed to dig it.

Here's [the code & data]() it picks through.

But, um...confession.  I got the code wrong.  I iterated over the wrong data set.
I iterated over the equivalent of the IMDB ratings, looking for matches in the queue data,
instead of the other way around.  In my case, I was supposed to iterate over the
candy data, looking for matches in the demo data I made up, trying to
discover who likes gum and who likes Starburst.
But I didn't; I did it backwards.
So...my calculations for standard deviations weren't made with the right data.
So the matches aren't right.

Well, except they are, but probably only accidentally.  Ah well.  I'll eventually live it down.
