# Annotation guidelines for SANT, Negation
March 2020

# Table of Contents

1. [Introduction](#introduction)
2. [Terminology](#terminology)\
2.2 [Cue](#cue)\
2.3 [Scope](#scope)
3. [Negation in Norwegian](#negation-in-norwegian)\
3.1 [Verbs](#verbs)\
3.2 [Prepositions](#prepositions)\
3.3 [Advers](#adverbs)\
3.4 [Conjunctions](#conjunctions)\
3.5 [Determinatives](#determinatives)\
3.6 [Pronouns](#pronouns)\
3.7 [Affixes](#affixes)
4. [Annotation procedure](#annotation-procedure)\
4.1 [Annotating cues](#annotating-cues)\
4.1.1 [Identifying cues](#identifying-cues)\
4.1.2 [Discontinuous cues](#discontinuous-cues)\
4.1.3 [Modality and cues](#modality-and-cues)\
4.2 [Annotating scope](#annotating-scope)\
4.2.1 [Resolving scope](#resolving-scope)\
4.2.1.1 [Main verb negation](#main-verb-negation)\
4.2.1.2 [Subordinate clauses](#subordinate-clauses)\
4.2.1.3 [Negation modifying subjects](#negation-modifying-subjects)\
4.2.1.4 [Negation modifying objects](#negation-modifying-objects)\
4.2.1.5 [Negation of adjectives in noun phrases](#negation-of-adjectives-in-noun-phrases)\
4.2.1.6 [Negation of predicative complements](#negation-of-predicative-complements)\
4.2.1.7 [Exception items](#exception-items)\
4.2.1.8 [Sentential adverbs and adverbs scoping over negation](#sentential-adverbs-and-adverbs-scoping-over-negation)\
4.2.1.9 [Negation raising](#negation-raising)\
4.3 [Complex problems](#complex-problem)\
4.3.1 [Dummy subject sentences](#dummy-subject-sentences)\
4.3.2 [Negation versus speculation](#negation-versus-speculation)\
4.3.3 [irrealis sentences](#irrealis-sentences)\
4.3.4 [modality scoping over negation](#modality-scoping-over-negation)\
4.3.5 [conditional sentences](#conditional-sentences)\
4.3.6 [negative polarity items](#negative-polarity-items)\
4.3.7 [subjects and scope-cue overlap](#subjects-and-scope-cue-overlap)\
4.3.8 [Finishing](#finishing)\
4.3.9 [negation cues that do not indicate negation](#negation-cues-that-do-not-indicate-negation)\
4.4 [Special cases](#special-cases)\
4.4.1 [fortsatt ikke and fremdeles ikke](#fortsatt-ikke-and-fremdeles-ikke)\
4.4.2 [ikke lenger](#ikke-lenger)
5. [Using Brat](#using-brat)\
5.1 [Cue (in Brat)](#cue-in-brat)\
5.2 [Scope (in Brat)](#scope-in-brat)\
5.3 [The "Negates" relation](#the-negates-relation)\
5.4 [The "Affixal" attribute](#the-affixal-attribute)
6. [Suggested annotation procedure](#suggested-annotation-procedure)


# Introduction
Negation annotation involves identifying negations within a given sentence. Several corpora with negation annotation have been created, but none for Norwegian so far. These annotation guidelines are mainly adopted from the Spanish SFU (Jiménez-Zafra et al., 2017), ConanDoyle-neg (Morante and Daelemans, 2021) and NegPar (Liu et al., 2018), and modified to suit Norwegian, and with some simplifications that will be discussed below. The descriptions are mainly based on the Bokmål standard since there are few typological differences between Bokmål and Nynorsk, but the guidelines also cover Nynorsk.


# Terminology

## Cue
The negation cue is the word that signals a negation. These are often common words such as *ikke* 'not', *aldri* 'never' or *ingenting* 'nothing', but they can also be complex such as *(på) ingen måte* '(in) no way'. Negation cues might also be morpological, i.e affixes such as *u-* 'un-' and -løs '-less'. There are also various lexical items that can function as negation cues, such as *la være å* 'refrain from'. "Lexical negation" in the sense of antonymy, as in seeing "bad" as a negation of "good" is *not* annotated. We use "lexical negation" to refer to negation using lexical items that are composed of elements that are not traditionally seen as negation items, such as *la være* (lit. 'let be') mentioned above, and *mangle* 'lack', and many more. These will be further discussed in the following guidelines. In this project we we do not annotate cases where modality is inseparable from negation, or cases of vaguely impled negation.

## Scope
The scope is the part of the sentence or clause that is affected by the negation cue. Perhaps somewhat confusingly, the scope of a cue can involve elements that might not feel negated, as is the case, for example, with subjects of a phrase. Other annotation efforts annotate the "event" of a negation, which more closely refers to the word that is more directly affected by the negation, but we have chosen not to annotate the event. The scope is defined differently according to different cues. These rules are described in more detail towards the end of the guidelines. 

# Negation in Norwegian
Descriptions of negation in Norwegian mostly talk about negation adverbs and quantors, and not much about lexical negation in the way we have defined it above. Several works have been written regarding placement of negation in V2-languages and other related phenomena. 
The following is a brief description of negation in Norwegian. For further information about negation in Norwegian, see for example Faarlund, Lie and Vannebo's Norwegian reference grammar (Faarlund et al., 1997).

Negation in Norwegian is often marked by the use of adverbs (most notably *ikke* 'not'), pronouns or determiners, but other parts of speech or phrases are also used. Like in English, affixal negation is possible, but there is also the question of to which degree affixal negation is equal to non-affixal negation. There is usually a slight difference, as in English. Affixal negation is marked nevertheless in this annotation scheme. *Ikke* has a slightly different placement compared to English, with it coming before the verb in subordinate phrases.

An exception to the above-mentioned lack of descriptions of Norwegian negation is the description of Norwegian negation found in Golden et al. (2014)'s Norsk som fremmedspråk. In addition to a detailed description of the system outlined above, they also mention some positive polarity items (også, til og med, attpåtil, fremdeles) and some negative polarity items (heller (ikke), (ikke) engang, (ikke) lenger), but only with a brief discussion. They devote a few sentences to negating verbs (nektende verb), and mention *nekte* 'deny', *benekte* 'deny', *negere* 'negate', *avslå* 'decline' and *takke nei* 'decline'. Lastly they mention that words from several word classes can be negated by the use of prefixes.

If we look at the ConanDoyle-neg corpus, we find that *not* accounts for roughly 31% of all negation cues, *no* (as a determiner) for 14%, *never* 6%, *nothing* 6% and *without* just below 3%. One difference between Norwegian and English in this regard is that certain combined forms, such as *cannot*, *won't* etc. are treated as single cues in ConanDoyle, but although these exist in spoken Norwegian, they are not used in formal writing, and are thus unlikely to be found in any great abundance.

The following is a list of some possible negation cues in Norwegian. The list is by no means exhaustive. See the respective descriptions below for details and examples for each cue.

## Verbs
* unngå + inf
* la være/late vere + inf
* mangle/vante

## Prepositions
* uten/utan + å/at
* uten/utan + N

## Adverbs
* ikke/ikkje
* aldri
* borte
* ei

## Conjunctions
* (h)verken/korkje 

## Determinatives
* ingen,intet,inga

## Pronouns
* ingenting
* ingen

## Affixes
* u-
* ikke-- 
* -løs,-løse,-løst/-laus,-lause,-laust
* -fri,-frie,-fritt


# Annotation procedure
The following chapters will describe the annotation procedure. Details concerning the software follow a more general discussion of how the sentences should be annotated. All sentences containing semantic negation are annotated, meaning that if there is any negation of the propositions in the sentence, it should be marked regardless of how it is expressed. All sentences containing semantic negation are annotated regardless of their earlier sentiment annotations, meaning that there will be some, but not complete overlap between the sentences marked for negation and those marked for sentiment in the corpus presented in Øvrelid et al. (2019) A sentence can further contain multiple negation cues and associated scopes. Inter-sentential negation (negation spanning several sentences) is not annotated, but in these cases the scope of the negation is seen as implicit, and the cue is marked as having no scope. As in answering "no" to a question the author has posed earlier.

## Annotating cues

### Identifying cues
We should look for the word that makes us understand that there is some negation. Cues are usually members of a relatively fixed group of words, see the list above for more details. It is important to be aware of that although cues are usually from this list, the words above can also be found in cases that do not indicate negation, such as in certain fixed expressions. The annotator must therefore perform a test to check whether there is actually negation. A rephrasing such as *det er ikke slik at...* 'it is not the case that...' can be useful in this case. If the rephrasing is only possible with "Det er lite sannsynlig at..." or something similar, then it is a case of speculation, and it is not marked in this annotation round. Note that negation should be a direct consequence of the negation cue, not just implied due to other factors. 

### Affixal cues
We allow the marking of affixal cues. Some possible affixes are mentioned in the list above. One thing to note when looking for affixal cues, is whether it actually indicates negation or not, which is also the case for other negation cues. Words with affixal negation cues tend to be semantically different from adverbial negation with *ikke*, but the annotators need not worry about this. Some problems are specific to certain cues. We do not mark cases that are clearly not negated in any way.

#### u- and mis-
The prefix *u-* in Norwegian largely corresponds to the English prefix 'un-', but when used with nominal roots it is also used in a series of words where it usually has the meaning "bad", such as *udyr* 'beast; pest, *uvær* 'bad weather', *uvenn* 'enemy; bad friend', *utøy* 'vermin', *ulempe* 'disadvantage',*uår* 'bad (crop) year', and many more. Most of these are nouns. The prefix mis-, which largely corresponds to English "mis-", tends to indicate "not correct" or "bad", and is not annotated in these cases. One can try to dismantle the word and see if the word without the affix is in fact what is negated. This is perhaps especially relevant for words that in most cases are borrowed as-is, but where the frequency of these borrowings make the speakers aware of the morphology, such as in words containing the affixes "im-", "-in", etc. and other graeco-latin vocabulary items. For example, in Norwegian, "impotent" is quite different from "ikke potent". "impotent" is therefore not annotated, but in cases with clear negation, they should be annotated. The annotators also need to be aware of words where the prefix has been lexicalised, and the original non-negated word is no longer part of the active lexicon.

#### -løs
The affix -løs '-less' is another common affix that often indicates negation in the sense of "not containing". Note that this ending will look different depending on the concordance with the noun it is modifying: -løs (f,m), -løst(n), -løse(pl,def).

#### Nominalized negated adjectives
Affixally negated adjectives can be nominalized. The resulting nouns should not be seen as cues. So 'ulykkelig' can be u\[lykkelig\], but the 'u' in *ulykkelighet* is not a cue. Another common case is "-løshet", which should not be treated as a cue, either.


### Discontinuous cues
Cues can be discontinuous. This most often happens in the case of (h)verken eller 'neither...nor'. Other coordinated expressions are not treated as having discontinuous scopes.

*verken* [x] *eller* [y]

*ikke* [x og y]


### Modality and cues
Various modal items can scope over the negation. In these cases, it is important to check whether the modality actually scopes over the negation, or visa versa. Although modals together with negation can result in speculative readings of the proposition, it is important to distinguish between speculation, with or without negation, in which the negation cannot be separated from the modality, as in *knapt* 'barely' and *neppe* 'doubtfully'. Which does not include any negation, and cases where the modality scope is separate and distinguishable from the negation scope, for example *kanskje ikke* 'maybe not', where the negation can be annotated separately from the modal adverb. The latter case should be annotated.

### Lexical negations with prepositions or particles
In the cases where particle verbs function as negation, or if a negation expression is commonly used with a certain suffix, as in the cases *fravær av* 'abscence of', *mangel på* 'lack of', *ingen av* 'noen of', the preposition or particle is not included in the cue nor in the scope. These could have been annotated together with their verbs as part of the cue, following the fact that they are in most cases higly lexicalised, but from a modelling perspective it is useful to have a limited set of cues. The variation that including the prepositions would lead to lower counts for a larger set of less frequent, but related, negation expressions.

## Annotating scope
The following parts discuss various problems related to defining the scope once a cue has been identified. 

### Resolving scope
The following part is about resolving the scope of a cue. Once the cue has been identified, the corresponding scope must be resolved. The scope is the part of the sentence or phrase that belongs to the negation. It is usually not limited to only one word, even though the main negation might be focused on a single word or a more restricted phrase (this is called the event in some treatments of negation).


#### Implicit scope
The scope of a cue can be implicit, meaning it is understood from context. In the context of this annotation effort, this usually refers to cases where the scope lies in another sentence, and not within the sentence in which the scope is. This most commonly happens with the interjection *nei* 'no'. An example of this can be seen below, taken from the Conan Doyle corpus:

```
*No* , sir , it crumbled all to bits after we moved it . (2.94 HoundOfTheBaskervillesch10.snt109)
```
No in the above example refers back to a sentence, and negates the proposition in it.

However, this also happens with other cues, perhaps especially *ingen* and *aldri*, for example  in incomplete sentences that refer back to other sentences.

#### Main verb negation
If the negation modifies the main verb of a sentence, the entire sentence is part of the scope. 

```
[Jeg spiser] *ikke* [fisk].
I don't eat fish.
```

#### Subordinate clauses
If the negation cue modifies a verb in a subordinate clause, the whole subordinate clause is in the scope except the subordinate particle. Note that the subordinating conjunction can be elided, as in the second example.

```
Frikjent serverer underholdningsdrama med høyt tempo, tydelig skuespill og lasser på med [ting] som *ikke* [er helt som vi først tror de er].
Frikjent serves entertainment drama with quick pace, clear acting and pile up with things that are not quite like we first think they are.
```

Here, *som* 'that' is not marked as part of the scope. Note that the noun being modified by the subordinate clause is the subject, and therefore it too should be included.

```
Alvorlig syke har kontakt med [noe de] *ikke* [kan flykte fra]  [...]
The seriously ill have contact with something they cannot escape from [...]
```
In this case, the subordinate conjunction "som" is elided, but the subordination is inferred and marked the same way as above.

#### Negation modifying subjects
If a negation cue directly modifies the subject of a sentence, the scope of the cue becomes the whole sentence.

*Ingen* [barn leker i parken].
No children play in the park.

#### Negation modifying objects
If a free-standing negation cue directly modifies the object of a sentence, the scope of the cue becomes the clause headed by the verb in the clause that the object is in. If there only is one verb, then that means the whole sentence is in the scope.\
However, If the object is modified by an adjective negated by an affix, then the scope of that affix is still just the noun phrase, not the whole sentence.

```
[Jeg spiste] *ingen* [epler i går].
I ate no apples yesterday.
```


#### Negation of adjectives in noun phrases
If an adjective in a noun phrase is negated, then the whole noun phrase is part of the scope. This also applies in the case of affixal negation.

```
[Små barn vet ] *ingenting* [om 90-tallet] [...]
```

```
[...] og [leverte] *ingen* [ stor prestasjon på venstresiden.]
```

#### Negation of predicative complements in copula sentences
If the predicative complement in a sentence with a copula verb (*være* 'is', *bli* 'become') is negated with a negative item, then the whole phrase is part of the scope. 

```
[Bilen er] *ikke* [rød].
The car is not red.
```

However, if the predicate is a noun phrase with an adjective negated by an affix, then only the predicate noun phrase is negated, not the whole sentence.

```
Dette er [en] *u*[interessant film].
This is an uninteresting film.
```
### Exception items
Exception items, such as *untatt* and *bortsett fra* should be annotated depending on whether they are already in the scope of a cue or not. Liu et al. () add on Morante et al. (2011)'s guidelines and suggest dividing them into two groups: exceptions to negated scopes ('exception to nothing') and exceptions to positive sentences ('exception'). This means that if they are used in a sentence with otherwise no negation cues, then that word itself should be marked as the cue, while it is not marked if it is inside of a negation scope already.

[Jeg likte] all maten, *untatt* [gulrøttene].

[Jeg likte] *ikke* noe av maten, untatt [laksen].

### Sentential adverbs and adverbs scoping over negation
If a sentence contains a sentential adverb, then this adverb is seen as scoping over the entire sentence. It is therefore not included in the scope of a cue even if the cue modifies the main verb of a sentence. Rephrasing the sentence might help.

```
Dessverre [kan jeg] *ikke* [hjelpe deg].
Unfortunately I can not help you.
```
In this case, we can rephrase the sentence in order to understand the scopes: "It is unfortunate that it is not the case that I can help you." Putting the negation first does not lead to the intended reading: "It is not the case that it is unfortunate that I can help you."

The same applies generally to all adverbs that scope *over* the negation, as in the following sentence:

```
Og [de seks syltynne skivene av serranoskinke] , garantert *ikke* [skåret for hånd , slik man ser skinkekokkene briljere på barene i Sevilla] , var først og fremst uforskammet dyre , mente Fredag .
```

In this sentence, there is an embedded sentence *garantert ikke skåret for hånd* that contains a negation *ikke*. Since the adverb *garantert* 'definately' scopes over the negation (It is definately so that it is not the case that...), it should not be part of the scope. 

### Negation raising
Negation raising is the phenomenon where a negator is "raised" further up in a syntactic tree, which in Norwegian means further towards the beginning of a sentence. What usually happens is that for some verbs, the negation is seemingly put on the verb in the main sentence, even though the negation only scopes over a subordinate sentence. This happens in Norwegian, as in English, with mental state verbs like *tro* 'believe;think'. For example, in the sentence *Jeg tror ikke han kommer i morgen* 'I don't think he will come tomorrow', the *thinking* takes place, it is not negated, but rather the subordinate phrase "han kommer i morgen". It is therefore the subordinate phrase that is negated, as in "Jeg tror han ikke kommer i morgen". 
```
Jeg tror *ikke* [det kommer til å regne ].
```


If the subject or verb of the subordinated clause is elided, then the scope has no subject/verb marked. We do *not* mark elements in the main clause in the case of neg raising from subordinated clauses with ellipsis.

```
Og da mener jeg *ikke* [ flashy studior med blinkende gulv og artister på storskjerm.]
```


### Dummy subject sentences
In Norwegian, as in other Scandinavian languages, it is very common to use what is called *presenteringssetninger* 'presentation sentences', in which the underlying subject is moved to the object position, and a formal, semantically void subject *det* or *der* 'it;there' works as the syntactical subject. As Faarlund notes: "Substantivfrasen på objektplassen er *potensielt subjekt*, som har syntaktiske eigenskapar felles både med subjektet og objektet. Det potensielle subjektet er altså ikkje subjekt i grammatisk forstand". (NRG, 828). We therefore follow them and do not treat the formal subject as the subject of the negated phrase. The underlying subject should be marked as part of the scope.

For example:
    
```
Det [er] *ikke* [noe mel igjen].
It is not any flour left.
There is no flour left.
```
Here, the cue is *ikke*, and the underlying, negated subject is *mel*.

```
Det [skjedde oss] *ikke* [noe i helga].
It happened us not anything in weekend.the
Nothing happened to us during the weekend.
```
Here, too, the cue is *ikke*, but the underlying subject is *oss*. 

### Apposition
Apposition in the form of titles, etc, should always be included in the scope of the noun phrase it is in when relevant.

## Complex problems
Here we will discuss some problems that involve both cues and scopes. 

### Negation versus speculation
Speculation is often treated together with negation. If we imagine a scale, with a proposition being true at one end of a scale, and it being untrue in the other end, then speculation is the space in between. In other words, speculation is indication of the probability of a proposition being true. Although difficult to separate completely from negation, speculation is not explicitly annotated in this project. Annotated expressions must entail full negation of a proposition and not simply its uncertainty.

Speculation markers include *neppe* 'unlikely; probably not', *nok* 'probably', *sikkert* 'probably'.

The following sentences are therefore *not* annotated as negation:

```
Det kommer neppe som noen overraskelse at vi liker de trådløse Sennheiser Urbanite-modellene [...]
It hardly comes as a surprise that we like the wireless Sennheiser Urbanite models [...]
```
```
Det er nok veldig lenge siden den var ute og svømte .
It is probably a long time since it was out swimming.
```
```
[...] men denne platen kommer neppe til å bli blant hans største kommersielle suksesser.(103580)
[...] but this record is unlikely to become one of his greatest commercial successes.
```
### Irrealis sentences
Several sentences might include a type of negation coming from the use of conditionals and similar structures. These cases lack negation cues (apart from the tense markers or conditionals, subjunctions, etc) and are not marked in this annotation effort.
```
[...] disse parodisk slitte virkemidlene gjør at jeg ler høyt på steder hvor jeg tror serieskaperne ønsker at jeg egentlig skal bli revet med.
These parodically worn-out means makes me laugh out loud in places where I think the creators of the series would have wanted me to actually be carried away.
```
This sentence can be interpreted as meaning something along the lines of "I was not carried away" or "I do not laugh where I should", but there are no specific cues.

### Modality scoping over negation
In the case of modal verbs or adverbs, the cue and scope is indicated as usual. This is different from cases where the modality, which might indicate speculation, is inseparable from the negation cue. The modal item is not annotated as part of the scope.

```
[Vi hadde] kanskje *ikke* [ventet oss Bertine Zetlitz og Jahn Teigen] , selv om det hadde vært festlig , men litt mer internasjonalt kunne det gjerne ha vært .
```

### Conditional sentences
As with cases with modal items, negation within conditional sentences is also marked as usual. 



### Negative polarity items
Negative polarity items are lexical entities that are used together with negation cues, and which render the sentence ungrammatical should the negation cues be removed. They can sometimes be used in interrogative sentences as well. They are included in the scope of the negation in this annotation scheme. In Norwegian, examples include  *noe* 'any', *noen* 'any', and combinations with these words like *noen gang*, *noen sinne* 'ever'. In some corpora these are annotated as a separate category, but in our case they are simply annotated as part of the scope. Since Norwegian prefers splitting negations where possible, this is quite common. Rather than having "Jeg spiste ingenting" one might also frequently find "Jeg spiste ikke noe". In the latter case, "noe" is part of the scope, not part of the cue. Expressions like "at all" are also included in these cases.

```
[Jeg lo] *ikke* [i det hele tatt].
I did not laugh at all.
```

Here, *i det hele tatt* 'at all' modifies the strength of the negation, but it is simply annotated as a part of the scope. 


### Subjects and scope-cue overlap
Normally, the subject of a clause should be annotated as part of the scope. The only exception is when the cue and scope overlap in pronouns such as *ingen* 'no-one' and *ingenting* 'nothing'. The negation cues are kept only as cues in this case, and not treated as part of the scope, while the rest is annotated as normal. The reason behind this is that from a modelling perspective it is useful to know that there are no cases of overlap between cue and scope in the corpus.

```
*Ingen* [spiser is] .
No-one eats ice-cream.
```

### Finishing
Verbs that indicate the end of actions or states are not marked as cues. These include avslutte, være ferdig med å, etc. These can be tricky as they indicate that an action is finished at some time, but we see this as separate from something being "untrue". It is important in these cases to separate between sentences that *imply* negation, such as finishing sentences, and sentences that by themselves indicate negation. *Jeg er ferdig med å spise* 'I am finished eating', is not a negation of "I am eating", but it does imply that the person speaking is no longer eating.

### Existing
Several lexical items can indicate the abscense of something. In many cases, these are treated as negations, but it is important to note that these can be more dependant on context. For example, the word "borte" (away) can indicate negation in cases like ..., but not in cases like "der borte" (over there).  In some cases these are multiword expressions, commonly including a preposition.
-fravær av\


### Negation cues that do not indicate negation
Cues that indicate negation may often also be used with a non-negated meaning. This can happen in fixed expressions, or with the cues themselves. The expressions can be rephrased to check if this is the case. Some examples follow below.

### ikke bare 
Although the phrase *ikke bare* 'not only' does not indicate negation of the words or phrases it modifies, we do annotate the negation in this expression because although the usage is clearly focusing, the meaning is compositional.

```
Jeg spiste ikke bare pizza, men fire hamburgere også!
I did not only eat pizza, but also four hamburgers!
```

One could think that *only pizza* is negated, in the sense that the hypothetical situation of only eating pizza is negated.

### Ingen hemmelighet at
Expressions like *ingen hemmelighet (at)* "it is a secret that...", *(det er) ingen tvil om (at)* 'there is no doubt that...' and related expressions do are similar to "ikke bare" in the sense that they are not used to negate the following expressions. Although it might seem unnatural to see these as negations, we chose to annotate them as such because of their compositionality. 

```
Det er ingen hemmelighet at nordmenn er et quiz-elskende folkeferd.
It is no secret that Norwegians are a quiz-loving people.
```

It does not mean that Norwegians are not a quiz-loving people. Note that these can be a bit difficult as it is somewhat strange to see it as a negation of "det er en hemmelighet at nordmenn er et quiz-elskende folkeferd". 

### Hvis ikke
The frequent combination *hvis ikke* 'if not; otherwise' contains the word *ikke*, but does not indicate negation, and is not marked as such. It is used to indicate the hypothetical outcome of the negation of something that has been previous mentioned, and this is outside the scope of this annotation effort.

```
Hvis ikke kommer jeg nok til å fortsette å le mer enn jeg blir grepet av Frikjents stadige høydramatiske vendepunkt.
If not, then I will continue to laugh more than get moved by Frikjents continuous dramatic turning-point.
```

Here, *hvis ikke* hypothetically negates the preceding sentence, and has no scope over the following sentences. Inter-sentential negation is not annotated.

This should not be confused with a negation within a conditional clause, as in "if I don't...", see the chapter on conditional clauses.


# Special cases

## Verken eller inside scope
Some items, like 'både...og' and 'også' have analoguous forms inside the scope of a negation, giving (h)verken...eller and heller. In the case where these forms are triggered by an outisde negation cue, they should not be annotated as being inside the scope. If verken...eller is not within the scope of another negation, then it is likely to be a cue.

## fortsatt ikke, fremdeles ikke
In some cases, it is not the continuation of the action, but rather the state or action itself that is being negated. If this is the case, the words *fortsatt* 'still' and *fremdeles* 'still' are kept outside of the scope. 


## Ikke lenger
In the case of *ikke lenger* 'no longer', 'no more', the word 'longer' is treated as being inside the scope. (the continuation of the act/state has been negated), as in the example below, taken from the Conan Doyle corpus. This is similar to the treatment of negation items, and the removal of the negation leads to an ungrammatical proposition. 

```
[The fact is] no [longer a secret] . (2.623 dog of baskerville 13.183)
```

## Quotes, titles and foreign languages
Negation that is found in titles and quotes should be annotated as normal as long as it is written in Norwegian. English lyrics and titles should not be annotated even if they contain negation.


# Using Brat

## Cue (in Brat)
The cue is an "Event" type. This is the first part that should be identified in a sentence. The cue can be both complex (multiword) and discontinous. Discontinous cues are created by first marking the first word of the cue, and then pressing the "add frag" button. Discontinuous cues are mainly annotated in the case of *(h)verken...eller..." 'neither...nor...'.* The cue option can be selected by pressing the shortcut key "c".

[image1]: images/ufrivillig.png "Labels"

![alt text][image1]
<br/>Example 1: affixal negation *


[image2]: images/mordgaaten.png "Labels"

![alt text][image2]
<br/>Example 2: Discontinuous spans *

  

## Scope (in Brat)
Once the cue has been identified, the scope can be marked, and a relation can be drawn from the cue to the scope. The scope of a cue can, as the cue, be both complex and discontinous. Both multiword scopes and discontinuous scopes are very frequent. The scope option can be selected by pressing the shortcut key "s".


## The "Negates" relation
Once the cue and scope has been established, the user can draw a relation from the cue to the scope. There is only one relation possible, which is the "Negates" relation. It can also be selected by pressing the shortcut "N".

## The "Affixal" attribute
Cues that are affixal in nature should be marked as such using the "affixal" attribute. This attribute is only used on cues, and has no hotkey associated with it. 

# Suggested annotation procedure
* Look for any known negation cues
* Pay close attention to affixal negation. This is often harder to spot quickly.
* Be aware of the differences in scope for affixal and free-standing negation.
* Is there any part of the sentence that is negated, but with no known cue?
** Try to identify what constitutes the part that negates the sentence
* Mark the cue
* Identify the span, according to the rules described.
* Pay attention to coordination and sentence adverbials




References
Faarlund et al.
Golden, Anne and Kirsti Mac Donald, Else Ryen (2014): Norsk som fremmedspråk: Grammatikk. 4. utgave. Universitetsforlaget. Oslo.

Øvrelid et al.
