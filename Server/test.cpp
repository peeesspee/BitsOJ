//Headers
#include <bits/stdc++.h>
#include <iostream>
//#include<boost/multiprecision/cpp_int.cpp>

//Macros
#define mod 1000000007
#define pi 3.1415326
#define ld long
#define ll long long
#define ull unsigned long long
#define big int128_t
#define pb push_back
#define pf push_front
#define mp make_pair
#define cs(i) c_str()[i]
#define loop(i,start_value,final_value) for(i=start_value;i<final_value;i++)
#define test_cases long test_;cin>>test_;while(test_--)
#define sfl(x) scanf("%ld",&x)
#define pfl(x) printf("%ld",x)
#define elif else if


//Functions
ll max(ll a,ll b){return a>b?a:b;}
ll min(ll a,ll b){return a<b?a:b;}
ll swap(ll a,ll b){ll t=a;a=b;b=t;}
ll gcd(ll a,ll b){if (b == 0)return a;return gcd(b, a % b);} 
ll lcm(ll x, ll y){return x*y/gcd(x,y);}
ll power(ll x,ll y,ll p=mod){ll res=1;x=x%p;while(y>0){if(y&1)res=(res*x)%p;y=y>>1;x=(x*x)%p;}return res;} 
bool is_prime(ld n){if(!(n&1)&&n!=2)return false;elif(n==2)return true;else for(ld i=3,s=sqrt(n);i<=s;i+=2){if(n%i==0)return false;}return true;}

//Namespaces
using namespace std;

int main(void)
{
    ios_base::sync_with_stdio(false);
	cin.tie(NULL);
	cout.tie(NULL);
	//Variables
	ld n;	
	test_cases
	{
	    
	    
	}
	return 0;
}
