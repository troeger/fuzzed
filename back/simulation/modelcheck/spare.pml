#define nPlaces 2
#define nTransitions 2
#define inp1(x1) (x1>0) -> x1--
#define inp1_2(x1, x2) (x1>0 && x2>0) -> x1--;x2--
#define inp1_3(x1, x2, x3) (x1>0 && x2>0 && x3>0) -> x1--;x2--;x3--
#define inp1Inhibited(x1, x2) (x1>0 && x2==0) -> x1--
#define inp1Inhibited2(x1, x2, x3) (x1>0 && x2==0 && x3==0) -> x1--
#define inp1Inhibited3(x1, x2, x3, x4) (x1>0 && x2==0 && x3==0 && x4==0) -> x1--
#define out1(x1) x1++

// marking, restricted to one token
bool Msparepassive 		= 1;
bool Mspareactive 		= 0;
bool Mspare_failed		= 0;
bool Mprimary_running 	= 1;
bool Mprimary_failed 	= 0;

bool fail = 0;

bool propagated0 = 0;
bool propagated1 = 0;

inline timedTransitions()
{
	if
    ::  d_step{ inp1(Mspareactive)->out1(Mspare_failed);skip }
    ::  d_step{ inp1Inhibited(Msparepassive, Mspareactive)->out1(Mspare_failed);skip }
    ::  d_step{ inp1(Mprimary_running)->out1(Mprimary_failed);skip }
	fi
}

inline immediateTransitions()
{
	if
    ::  d_step{ inp1_2(Mprimary_failed, Msparepassive) -> out1(Mspareactive); propagated0++;skip }
    ::  d_step{ inp1_2(Mprimary_failed, Mspare_failed) -> propagated1++; out1(fail);skip }
	fi
}

active proctype net()
{
 	do
	:: timedTransitions(); immediateTransitions(); skip
	:: timeout -> break
    od
}

ltl {always(Mprimary_failed -> !fail U Mspareactive)}