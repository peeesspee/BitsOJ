#include <bits/stdc++.h>
#include <chrono> 

using namespace std;
using namespace std::chrono; 


typedef long long LL;

/* Matrix Exponentiation */

#define MS 105
#define MOD 1000000007

int main()
{
	freopen("t1.in","r",stdin);
	freopen("t2.ans","w",stdout);
	int t;
	scanf("%d",&t);
	
	//auto start = high_resolution_clock::now(); 

	while(t--)
	{
		long long X, T1, T2, K, N;
		long long data[1000006],i,j;
		cin>>X>>T1>>T2>>K>>N;
		//N--;
		data[0]=X;
		for(i=1;i<=T1;i++)
		{
			data[i]=data[i-1]+1;
		}

		for(i=1+T1;i<=T1+T2;i++)
		{
			data[i]=((data[i-1]%MOD)*2)%MOD;
		}
		if(N<1+T1+T2)
		{
			cout<<data[N-1]%MOD<<endl;
		}
		else
		{
			for(i=1+T1+T2;i<=N;i++)
			{
				long long prod;
				for(prod=1,j=i-1;j>=i-K;j--)
				{
					prod = ((prod%MOD)  * (data[j]%MOD))%MOD;
				}
				data[i] = prod % MOD;
			}	
			cout<<data[N-1] % MOD<<endl;
		}
	
	}
	auto stop = high_resolution_clock::now(); 
	auto duration = duration_cast<milliseconds>(stop - start); 
    cout << "Time taken by function: "<< duration.count() << " milliseconds" << endl; 
  
	return 0;
}
