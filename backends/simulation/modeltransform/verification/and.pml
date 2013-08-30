#define NPLACES 5

// marking of the net
bool p[NPLACES];

// transition conditions
#define enabled_t0 (p[0])
#define enabled_t1 (p[1])
#define enabled_and (p[2] && p[3])

// failure condition
#define systemFailure (p[5])

// firing
#define fire_t0 	p[0] = 0; p[2] = 1;
#define fire_t1 	p[1] = 0; p[3] = 1;
#define fire_and 	p[2] = 0; p[3] = 0; p[4] = 1;

active proctype NetBehaviour()
{
	int count = 0;
	do
		:: enabled_t1 ->
			count++; 
			fire_t1
		:: enabled_t0 ->
			count++;
			fire_t0
		:: enabled_and ->
			count++;
			fire_and
	od;
}