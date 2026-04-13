

### Objectives

The decisive evidence: Apple Photos, Google Photos, and Notion all gave up on header injection. Day One uses zip-with-manifest. Header injection is a maintenance nightmare with silent failure modes.

Ready for next move when you are. The roadmap suggests Phase 0 (schema finalization) next, but you might want to address the open questions first or kick off parallel

### Notes

Thoughts on knowledge

Rhetorical Situation

What is it that the target reader wants?
Who are they?
What is their current work around?

References
- Working Backwards Process (WorkingBackwards.Process.WebHome) - XWiki
- [https://w.amazon.com/bin/view/WorkingBackwards/Process](https://w.amazon.com/bin/view/WorkingBackwards/Process)
- Value Proposition Design Book - Preview & Download PDF
- [https://www.strategyzer.com/library/value-proposition-design-2](https://www.strategyzer.com/library/value-proposition-design-2)

Research Bookmark on Feeling Stupid

What are the measurable claims, statements, findings etc. that are testable in any given paper?

Claims, Hypotheses, Assumptions etc. We want to build out the full ontology 

Delineate between ontology and taxonomy and any other relevant lattices which would serve to help the agents 
How does this associate to siloed context windows? When should they be joined and segmented? 
Are there levels in between ?


What is the User Journey of interfacing with the AIs?

1) Who is the user "holding" the AIs?
2) What do we know about that user?
3) What does the user state they want to do?
	1) How do their actions compare?
4) Relative to the stated objective of the user, does it include or intend to influence other humans?
5) What do we know about the target reader?
	1) =={--Insert Arese Architecture and Questions Here--}==



~~Think about Internal Answers and James digest - Sent to IA creator~~ 


Place holder

the list from kevin will drive the MVP and UVP of pebbles v0

We need to further intersect the articles between the no escape and the recent thanks from LangChain on Memory 

Further intersect my thoughts on the origins and ingestion of knowledge before they become memories 

Plus what Geoff is pushing with new AI coding languges and the prior lang that shapped software eng.

intersect this with IKE (e.g. the CoWork-Lite LLM Model Wrapper Explosion)


THe article on running seems to be an excellent out of echo chamber example we should use for both Pebbles and Arese




```
 1) **Option C: Both** -- CLI as the core, importer as the first ingestion surface.

  Why are you calling it importer?

  Explicity integrations will leverage the following repos

  /Users/ljack/github/defuddle
  /Users/ljack/github/obsidian-clipper

  During design we must decide how best to intercept to introduce addtional YAML attributes per Pebbles spec. Could this be done by a simple fork?

  2) we don't have any integration friction with anyone for proof of concept. language choice for the intercept must be driven by the dependency on clipper and/or
  defuddle. Please investigate the code bases and confirm if both or only one is required and what lanugage makes the most sense for pebbles yaml attribute insertion.

  The CLI MUST be stand alone and should implement pebbles for all non browser surfaces e.g. screenshots, images, docs, etc. This also enables Agents simple interfaces
  to create pebbles for any artifact.

  Need to evaluate the pros and cons of taking a .zip/tar/gz like approach which envelops/compresses the artifact yet still allows for instant accssess to the yaml
  frontmatter a hybrid if you will that keeps everything togteher

  -vs- attempting to do "cute things" to the MIME/file headers with full backward compatibility. needs research if it's possible to reliably store YAML/JSON etc. in
  file headers

  3) Yes. "Red strings on Ekman 8 emotions, 5 uku_types, and 4 intents could score significantly higher while maintaining b=0, FA=0."

  we should also evaluate any reserach which touched on kinetic "red strings" e.g. attributes vs non-kinetic that seems to be a powerfull delineator to significantly
  reduce search spaces as this will be easy to infer / recall during query (e.g. was it an action or a thought?)

  4) Yes exactly stems from his post which confirms a huge design direction for us

  "the design principle behind what we're shipping with ByteRover's Memory Swarm federated search across BM25, wikilink graph expansion, and hybrid vector+keyword,
  fused with RRF. Each retrieval method has uncorrelated blind spots. BM25 misses paraphrases, embeddings miss exact terms, graph traversal misses unlinked knowledge.
  The ensemble doesn't eliminate failure, it decorrelates it."

  fully clarify all acronyms RRF etc with definitions for all of these terms incl LoCoMo (Long-term Conversational Memory) in an appendix glossary
  investigate full repo /Users/ljack/github/defuddle/Users/ljack/github/locomo

  evaluations will be a HUGE aspect of pebbles as validated by the recent paper no-escape

  also ensure the paper is copied into /Users/ljack/Library/Mobile Documents/iCloud~md~obsidian/Documents/m31uk3/_m31uk3/uku-pebbles/_research/_papers

  however you implementation question is unclear. if pebbles is the schema and the ingestion tooling e.g. cli and fork of clipper/defuddle. then we need to think
  carefully about the integration end points for ByteRover and anyone else. this seems to be a question of existing data ingestion e.g. converting non pebblized content
  into pebblized content and allowing exposing that function call as an endpoint e.g. mcp, cli, api etc.

  we need to think carefully on the value of that. as per Q2 if we develop a novel MIME/file header solution there could be value in that; however regardless non of
  this will be the Pebbles moat or "stickiness" in the market. the true uvp comes from two things: mindful 1) attributes e.g. 8 emotions, 5 uku_types, and 4 intents
  (these need finalization) and precise execution of the schemaw hich unlocks new measurable performance provable via evals like LoCoMo. and 2) rapid mass market
  adoption similar to that of Agents.md and Skills.md

  as soon as critical mass is reached in market attention/adoption there will be a million new end points that can implement/create pebbles in the same way that there
  are infinte ways to create Skills and Agents .mds.

  consider all of this to determine the opportunity / LOE costs of buliding said functionality -vs- leaving it open. as long as the spec is open the community can
  implement it directly into systems like ByteRover or anything else. this is distinct from our organic ingestion push (which in and of istsellf will long term be
  replaced by native implemention into OS/device owerns e.g. Mac OS, Android, iOS and replace the feckless functionality that exists today) Again pebbles intends to be
  the blueprint for the future not the product itself.

  inspiration:

  "\> If you want your writing to still be readable on a computer from the 2060s or 2160s, it’s important that your notes can be read on a computer from the 1960s.

  You should want the files you create to be durable, not only for posterity, but also for your future self. You never know when you might want to go back to something
  you created years or decades ago. Don’t lock your data into a format you can’t retrieve."

  /Users/ljack/Library/Mobile Documents/iCloud~md~obsidian/Documents/m31uk3/Clippings/Thread by @kepano - File over app.md

  **Sub-question:** Have you discussed integration mechanics with Andy? Is there a preferred protocol (REST, MCP, direct library call)?

  breifly via X.com messages. totally possible to reach out to him again, but I'd like to have something valuable that I can offer him for free (e.g. working demo). I
  have zero concern that he takes it for himself, I have parrallel "ponies" I'm working with to release pebbles into the wild. a crude analogy I'm intending to have
  multiple "infection" vectors to have the highest likelihood of pebbles going viral and gaining mass market adoption.

  5) this sounds directionally correct minus the chrome extension limit as stated above

  esentially we're solving for two key killer features in parallel

  6) ingestion with near zero friction for users and agents that covers both browser surface and CLI (e.g. user invocation via agent and automous agent invocation)
  7) proving the schema and well designed researched attributes of pebbles maximize on user empathy such that they create powerful facets with which users and agents
  can significantly reduce search spaces and effortlessly create links between pebbles (e.g. the google maps location history for knowledge work)
```