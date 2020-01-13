#include <iostream>
#include <cstdio>
using namespace std;
typedef long long LL;
const int maxn=1001;
const LL inf=1LL<<60;
int a[maxn];
int n;
LL sum[maxn];
#define S(l,r) (sum[r]-sum[l])
int main(){
	scanf("%d",&n);
	for(int i=1;i<=n;i++){
		scanf("%d",&a[i]);
		sum[i]=sum[i-1]+a[i];
	}
	LL ans=-inf;
	LL ansl,ansm,ansr;
	for(int i=0;i<=n;i++){
		LL mx1=-inf,mx2=-inf;
		int l,r;
		for(int j=0;j<=i;j++){
			LL tmp=S(0,j)-S(j,i);
			if(tmp>mx1){
				mx1=tmp;
				l=j;
			}
		}
		for(int j=i;j<=n;j++){
			LL tmp=S(i,j)-S(j,n);
			if(tmp>mx2){
				mx2=tmp;
				r=j;
			}
		}
		if(ans<mx1+mx2){
			ans=mx1+mx2;
			ansl=l;
			ansr=r;
			ansm=i;
		}
	}
	cout<<ans<<endl;
	return 0;
}