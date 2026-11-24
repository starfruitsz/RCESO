### Definition 1 (EID)
rthereferenceinput. Definition 1: Let the control input be u(t)=0. Then, the On the other hand, since the disturbance is assumed to be output of the plant (1) for the disturbance d(t) is y o (t), and unknown, no internal model of it is contained in the control theoutputoftheplant(2)forthedisturbanced e (t)isy(t).The system, and we need to devise a method of suppressing its disturbance d e (t) is called an EID of the disturbance d(t) if influence on the output. Note that the EID estimator makes y(t)≡y o (t)forallt≥0. use of the state observer instead of the inverse dynamics of Let the plant. This is a big difference in system structure between the disturbance-observer method and the one presented in this Φ={p (t)sin(ω t+φ )}, i=0,...,n, n<∞ i i i paper. (3) InFig.3,forthestateobserver where ω (≥0) and φ are co

### Assumption 1
ctly used to obtain Assumption1: (A,B,C)iscontrollableandobservable. anEID.However,sincethislemmaclarifiesthatanEIDexists, Assumption2: (A,B,C)hasnozerosontheimaginaryaxis. itgivesusatheoreticalguaranteeofthemeaningfulnessofEID Remark 1: Assumption 1 is for simplicity. Since we want estimation. In the next section, we devise a simple method of to use a control input to improve the tracking performance of estimatinganEID. the output, if 

### Assumption 2
iesthatanEIDexists, Assumption2: (A,B,C)hasnozerosontheimaginaryaxis. itgivesusatheoreticalguaranteeofthemeaningfulnessofEID Remark 1: Assumption 1 is for simplicity. Since we want estimation. In the next section, we devise a simple method of to use a control input to improve the

### Lemma 1
othefollowinglemma. Lemma 1: Under Assumptions 1 and 2, there always exists andsubstitutingitinto(2)yields an EID d (t)∈Φ on the control input channel of the distur- e banced(t)imposedontheplant(1),andtheoutputitproduces xˆ˙(t)=Axˆ(t)+Bu(t)+{Bd (t)+[∆x˙(t)−A∆x(t)]}. e belongstoΦ. (7) Authorized licensed use limited to: YANGZHOU UNIVERSITY. Downloaded on November 24,2026 at 10:03:06 UTC from IEEE Xplore. Restrictions apply. 382 IEEETRANSACTIONSONINDUSTRIALELECTRONICS,VOL.55,NO.1,JANUARY2008 Fig.3. Configurationoftheimprovedservosystem.
