# Draft talk-page post — [Talk:Strategic voting](https://en.wikipedia.org/wiki/Talk:Strategic_voting)

Companion to [star-strategy-pages-vs-wikipedia.md](star-strategy-pages-vs-wikipedia.md). **Not posted** — this is a draft for you to post from your own account, after adjusting the disclosure line to describe your actual involvement.

## Read the room first

The December 2024 thread [§ Removal of sources](https://en.wikipedia.org/wiki/Talk:Strategic_voting#Removal_of_sources) is the single most important thing to know before posting. Wotwotwoot added Ogren 2024 (*Electoral Studies*) and Robinette 2023 (*Constitutional Political Economy*); Affinepplan removed them as "essentially SPS," called them "amateurish," and pinged two domain experts. DominikPeters replied that both journals are genuinely peer-reviewed but that the papers are **primary sources** ([WP:PSTS](https://en.wikipedia.org/wiki/Wikipedia:No_original_research#Primary,_secondary_and_tertiary_sources)) — "some particular simulation with a thousand arbitrary choices" — and suggested the fix is attributed, hedged phrasing: *"In some simulations on random data, Condorcet methods incentivize..."*

Two things follow.

**Wolk, Quinn & Ogren 2023 will get the same treatment.** Same journal as one of the removed papers, one shared author, and a paper about STAR co-authored by the executive director of the organization promoting STAR. Lead with it and the thread reruns. It also carries a published correction notice — better that we cite it ourselves than have someone find it.

**Our verified counterexamples are unusable.** Everything in `code/star-strategy/verify.py` is [original research](https://en.wikipedia.org/wiki/Wikipedia:No_original_research). And the very first thread on that talk page has an editor complaining about "small sets of contrived, anecdotal examples." Offering constructed profiles would confirm the worst assumption about where the post is coming from. The draft says so explicitly, which turns a liability into a credibility signal.

So the post leads with two sourcing problems that have nothing to do with STAR — including a flat internal contradiction anyone can check in thirty seconds — and puts the STAR addition last, pre-hedged, with a fallback that drops the contested claim entirely. Points 1 and 2 are likely to land on their merits. Point 3 is a coin flip, and the fallback is the part worth fighting for.

---

## The draft

Paste as a new section at the bottom of [Talk:Strategic voting](https://en.wikipedia.org/wiki/Talk:Strategic_voting). `~~~~` expands to your signature automatically.

```wikitext
== Rated rules with an elimination stage: two sourcing issues, one proposed addition ==

'''Disclosure:''' I have a [[WP:COI|conflict of interest]] here — I am a volunteer contributor to software used by the Equal Vote Coalition, which advocates for [[STAR voting]]. I am not editing the article and will not; this is a request. I have read the [[Talk:Strategic voting#Removal of sources|December 2024 thread]] and have tried to write points 1 and 2 so they stand or fall without reference to any of that, and point 3 so it can be accepted in a form that cites nothing contested.

Points 1 and 2 are about the [[Strategic voting#Common types of strategic voting|Common types]] section and need no new sources.

'''1. Score voting is listed as both affected by and immune to compromising, citing the same source at the same location.''' In the ''Compromise'' entry:

* ''Also affected:'' Borda, '''Score''', approval voting.<ref name="Armytage-SVN" />{{rp|at=prop. 4, note}}
* ''Immune:'' Coombs' method, antiplurality, rated voting rules (e.g. '''score voting''')

Both lines cite Green-Armytage 2014 at prop. 4's note. One of them is a misreading. Could an editor with the paper to hand check which? I would guess the note distinguishes cases the two lines have collapsed, but I have not read it and am not proposing a fix I can't source.

'''2. The pushover immunity claim is uncited and broader than its examples.''' The ''Turkey-raising'' entry ends:

* ''Immune:'' Plurality and all commonly-used rated voting systems, including score voting and approval voting.

No citation is attached. The reasoning is clear enough for the two methods named — neither has an elimination stage for a pushover strategy to exploit — but "all commonly-used rated voting systems" is a wider claim than that reasoning supports. Rated methods with an elimination stage are in use: [[STAR voting]] scores candidates, advances the top two, then decides between them by majority preference, and has been used for the Independent Party of Oregon's 2020 primary and for a large number of private organizational elections. Whether a pushover strategy is available there is a separate question I am not asking the article to answer — the request is just that the sentence be narrowed to the methods it can support, or given a citation for the general claim.

Compare the ''Abstention'' entry, which handles this correctly: it says "point-summing systems (i.e. score voting and positional voting)" and cites Balinski and Laraki. That is the right shape.

'''3. Proposed addition to [[Strategic voting#Cardinal single-winner voting|Cardinal single-winner voting]].''' The section opens "Most cardinal, single-winner voting systems in large elections encourage similar strategies" and gives the approval-threshold result: top-rate above-average utility, bottom-rate the rest. That derivation assumes scores are aggregated once and the highest total wins. It doesn't describe rated methods where the scores instead select a set of finalists, since there the question is which candidates advance rather than where to put an approval cutoff. The section currently has no sentence covering that case. Proposed, after the "semi-honest exaggeration" paragraph:

<blockquote>Rated methods that use scores to select finalists rather than to determine the winner outright do not follow this pattern, because the relevant question for a voter becomes which candidates advance rather than where to set an approval threshold. In [[STAR voting]], the two highest-scoring candidates advance to an automatic runoff decided by majority preference between them. In simulations on random electorates, Wolk, Quinn and Ogren report that this reduces the incentive for voters to consider candidate electability relative to plurality voting.<ref>{{cite journal |last1=Wolk |first1=Sara |last2=Quinn |first2=Jameson |last3=Ogren |first3=Marcus |title=STAR Voting, equality of voice, and voter satisfaction: considerations for voting method reform |journal=Constitutional Political Economy |volume=34 |issue=3 |pages=310–334 |date=2023 |doi=10.1007/s10602-022-09389-3 |doi-access=free}} A correction was published as {{doi|10.1007/s10602-023-09426-9}}.</ref></blockquote>

On the source, so nobody has to dig: it is peer-reviewed and open access, it is a simulation study and therefore a primary source under [[WP:PSTS]], the lead author is the executive director of the organization that promotes the method, and a correction notice was published in December 2023. The in-text attribution and the "in simulations on random electorates" hedge follow the phrasing {{u|DominikPeters}} proposed in the December 2024 thread for exactly this class of source.

'''If that last sentence is the sticking point, drop it.''' The first two sentences are a mechanical description of how the method tabulates, they need no simulation study, and they are what actually fills the gap in the section. I would rather have those than nothing.

What I am '''not''' proposing: any claim that STAR resists strategy in general, any criterion-compliance claim, and any worked example. I have constructed examples of my own and they are [[WP:NOR|original research]] — I mention them only to say I know they don't belong here.

Happy to convert whichever of these gets agreement into a formal {{tl|edit COI}} request with exact before/after wording. ~~~~
```

## Before you post

- [ ] Rewrite the disclosure to match your actual relationship to Equal Vote — "volunteer contributor to software used by" is my guess from the bettervoting work, not something you told me. Understating it is the one unrecoverable mistake here.
- [ ] Decide whether to post all three points together or split them. Together is honest about where the post comes from; splitting points 1–2 into their own section would get them judged on merit, but posting the STAR request separately afterwards looks like a setup. I'd keep them together.
- [ ] Check whether Green-Armytage 2014 prop. 4's note actually resolves point 1 before you post it — if it plainly supports one line over the other, say which and the fix is trivial.
- [ ] Confirm the Independent Party of Oregon 2020 claim is sourced somewhere citable, or cut the clause. It's currently doing rhetorical work ("commonly-used") and is the one factual assertion in the post that a hostile reader would check first.
- [ ] Expect Affinepplan. Point 3 is the target; points 1 and 2 are defensible on their own and shouldn't be conceded as a package deal if point 3 is rejected.
