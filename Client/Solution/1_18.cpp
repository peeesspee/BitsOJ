#include<bits/stdc++.h>
using namespace std;


struct Graph{
	int V,E;

	vector<pair<int,pair<int,int>>> edges;
	Graph(int V,int E){
		this->V = V;
		this->E = E;
	}

	void add_edge(int u,int v,int w){
		edges.push_back({w,{u,v}});
	}

	int Kruskal_MST();
};

struct DisjointSets{
	int *parent , *rnk;
	int  n;

	DisjointSets(int n)
	{
		this->n = n;
		parent = new int[n+1];
		rnk = new int[n+1];

		for(int i =0;i<=n;i++)
		{
			rnk[i] = 0;
			parent[i] = i;
		}
	}

	int find(int u){
		if(parent[u] != u)
			parent[u] = find(parent[u]);
		return parent[u];
	}

	void merge(int x, int y){
		x = find(x); y= find(y);
		if(rnk[x]>rnk[y])
			parent[y] = x;
		else
			parent[x] = y;
		if(rnk[x] == rnk[y])
			rnk[y]++;
	}

};

int Graph::Kruskal_MST()
{
	int mst_wt = 0;

	sort(edges.begin(),edges.end());

	DisjointSets ds(V);

	vector<pair<int,pair<int,int>>>::iterator it;
	for(it=edges.begin();it!=edges.end();it++)
	{
		int u = it->second.first;
		int v = it->second.second;

		int set_u = ds.find(u);
		int set_v = ds.find(v);

		if(set_u != set_v){
			cout<<u<<" _ "<<v<<endl;
			mst_wt+=it->first;
		}
		ds.merge(set_u,set_v);
	}
	return mst_wt;
}



int main() 
{ 
   while(1)
	{ cout<<"5\n"; }
    return 0; 
}