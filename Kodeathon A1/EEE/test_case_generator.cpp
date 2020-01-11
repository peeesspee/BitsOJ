#include<bits/stdc++.h>
using namespace std;

#define ll long long



int main(void){
	srand(time(NULL));
	freopen("input05.in","w",stdout);
	ll t=40,n=100000,i,j,k,a[200005],x,y;
	for(i=0;i<2*n - 1;i++)
	{
		a[i] = i+1;
	}
		k=50000;
		cout<<n<<endl;
		while(k--)
		{
			x=(rand()%100000) - 1;
			y=100000 + (rand()%100000) - 1;
			a[x] = a[x] + a[y];
			a[y] = a[x] - a[y];
			a[y] = a[x] - a[y];
		}
		for(i=0;i<2*n - 1;i++)
		{
			cout<<a[i]<<" ";
		}
		cout<<endl;
}