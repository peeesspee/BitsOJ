#include <iostream>
using namespace std;
int dp[3001][2],n,a[3001],b[3001],c[3001];
int main()
{
	int i;
	cin>>n;
	for (i=1;i<=n;i++) cin>>a[i];
	for (i=1;i<=n;i++) cin>>b[i];
	for (i=1;i<=n;i++) cin>>c[i];
	dp[1][0]=a[1];dp[1][1]=b[1];
	for (i=2;i<=n;i++)
	{
		dp[i][0]=min(dp[i-1][0]+b[i],dp[i-1][1]+a[i]);
		dp[i][1]=min(dp[i-1][0]+c[i],dp[i-1][1]+b[i]);
	}
	cout<<dp[n][0]<<endl;
	return 0;
}