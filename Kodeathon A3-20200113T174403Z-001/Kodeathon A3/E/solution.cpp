#include <sstream>
#include <fstream>
#include <cstdio>
#include <iostream>
#include <algorithm>
#include <vector>
#include <set>
#include <map>
#include <string>
#include <cstring>
#include <stack>
#include <queue>
#include <cmath>
#include <ctime>
#include <utility>
#include <cassert>
#include <bitset>
#define ll long long
#define mod 1000000007
using namespace std;
const int maxn=1000010;
struct in{ int l,r,id; }s[maxn];
bool cmp(in a,in b){ if(a.l!=b.l) return a.l<b.l; return a.r>b.r; }
int L,R,ans,a[maxn];
priority_queue<int,vector<int>,greater<int> >q;
int main()
{
	int N,K,i,j;
	scanf("%d%d",&N,&K);
	for(i=1;i<=N;i++){
		scanf("%d%d",&s[i].l,&s[i].r);
		s[i].id=i;
	}
	sort(s+1,s+N+1,cmp);
	for(i=1;i<=N;i++){
		q.push(s[i].r);
		while(q.size()>K) q.pop();
		if(q.size()==K&&q.top()-s[i].l+1>ans) L=s[i].l,R=q.top(),ans=R-L+1;
	}
	printf("%d\n",ans);
	return 0;
}