

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
    /* Let us create above shown weighted 
       and unidrected graph */
    int V = 9, E = 14; 
    Graph g(V, E); 
  
    //  making above shown graph 
    g.add_edge(0, 1, 4); 
    g.add_edge(0, 7, 8); 
    g.add_edge(1, 2, 8); 
    g.add_edge(1, 7, 11); 
    g.add_edge(2, 3, 7); 
    g.add_edge(2, 8, 2); 
    g.add_edge(2, 5, 4); 
    g.add_edge(3, 4, 9); 
    g.add_edge(3, 5, 14); 
    g.add_edge(4, 5, 10); 
    g.add_edge(5, 6, 2); 
    g.add_edge(6, 7, 1); 
    g.add_edge(6, 8, 6); 
    g.add_edge(7, 8, 7); 
  
    cout << "Edges of MST are \n"; 
    int mst_wt = g.Kruskal_MST(); 
  
    cout << "\nWeight of MST is " << mst_wt<<endl; 
  
    return 0; 
}