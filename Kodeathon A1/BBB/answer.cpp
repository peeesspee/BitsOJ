#include <bits/stdc++.h>
using namespace std;

int main() {
	freopen("t1.in","r",stdin);
	freopen("t1.ans","w",stdout);
	int t;
	cin>>t;
	while(t--)
	{
	    int n;
	    cin>>n;
	    int b;
	    map<int,int> mp;
	    for(int i=0;i<n;i++)
	    {
	        cin>>b;
	        if(mp.find(b)==mp.end())
	        mp[b]=1;
	        else
	        mp[b]++;
	    }
	    map<int,vector<int>> mp1;
	    for(auto i:mp)
	    {
	        mp1[i.second].push_back(i.first);
	    }
	    vector<int>::iterator it;
	    for(auto i:mp1)
	    {
	        cout<<i.first<<endl;
	        for(it=i.second.begin();it<i.second.end();it++)
	        {
	        cout<<*it<<" ";
	        }
	        cout<<endl;
	    }
	}
}
