#define nPlaces 2
#define nTransitions 2
#define inp1(x1) (x1>0) -> x1--
#define inp1_3(x1, x2, x3) (x1>0 && x2>0 && x3>0) -> x1--;x2--;x3--
#define inp1Inhibited(x1, x2) (x1>0 && x2==0) -> x1--
#define inp1Inhibited2(x1, x2, x3) (x1>0 && x2==0 && x3==0) -> x1--
#define inp1Inhibited3(x1, x2, x3, x4) (x1>0 && x2==0 && x3==0 && x4==0) -> x1--
#define out1(x1) x1++

// marking, restricted to one token
bool Mactive0 = 1;
bool Mactive1 = 1;
bool Mactive2 = 1;

bool Mfailed0 = 0;
bool Mfailed1 = 0;
bool Mfailed2 = 0;

bool M0 = 0;
bool M01 = 0;
bool M012 = 0;

bool fail = 0;

// counting the firings of immediate transitions (fire once. can be build with inhibitor easily)
bool propagated0 = 0;
bool propagated1 = 0;
bool propagated2 = 0;


inline timedTransitions()
{
	if
    ::  d_step{ inp1(Mactive0)->out1(Mfailed0);skip }
    ::  d_step{ inp1(Mactive1)->out1(Mfailed1);skip }
    ::  d_step{ inp1(Mactive2)->out1(Mfailed2);skip }
	fi
}

inline immediateTransitions()
{
	if
    ::  d_step{ inp1Inhibited3(Mfailed0, M01, M012, propagated0)   	-> propagated0++; out1(Mfailed0); out1(M0); skip }
    ::  d_step{ inp1Inhibited2(Mfailed1, M012, propagated1)  		-> propagated1++; out1(Mfailed1); out1(M01);skip }
    ::  d_step{ inp1Inhibited(Mfailed2, propagated2)         		-> propagated2++; out1(Mfailed2); out1(M012); skip }
    ::  d_step{ inp1_3(M0, M01, M012) 								-> out1(fail); assert(Mfailed0 && Mfailed1 && Mfailed2); skip }
	fi
}

active proctype net()
{
 	do
	:: timedTransitions(); immediateTransitions(); skip
	:: timeout -> break
    od
}

ltl {always((Mfailed1 && !Mfailed0) -> !<>fail) && always((Mfailed2 && !Mfailed1) -> !<>fail)}