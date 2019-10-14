#include<bits/stdc++.h>
using namespace std;

class ugraph
{
	private:
		int node_count;
		vector<pair<int,int>> *head;
		vector<pair<int,int>> :: iterator it;
		bool *visited;
		void unvisit()
		{
			for(int i=0;i<node_count;i++)
				visited[i] = false;
		}
	public:
		ugraph(int nodes)
		{
			node_count = nodes;
			head = new vector<pair<int,int>>[nodes];
			visited = new bool[nodes];
		}

		void add_edge(int,int,int=0);
		void show();
		void dfs(int);
		void bfs(int);
};


void ugraph::add_edge(int x,int y,int w)
{
	head[x].push_back(make_pair(y,w));
	head[y].push_back(make_pair(x,w));
	return;
}

void ugraph::show()
{
	pair<int, int> data;
	cout<<"Graph:\n";
	cout<<"Node   ::    Connections(Weight)\n";
	for(int i=0;i<node_count;i++)
	{
		cout<<"   "<<i<<"    ::    ";
		for(it = head[i].begin();it != head[i].end();it++)
		{
			data = *it;
			cout<<data.first<<"("<<data.second<<")"<<" -> ";
		}
		cout<<endl;
	}
}



void ugraph::dfs(int location)
{
	unvisit();
	stack<int> stk;
	stk.push(location);
	pair<int, int> data;

	while(!stk.empty())
	{
		location = stk.top()
		stk.pop()
		if(visited[location] == false)
		{
			cout<<location<<" ";
			visited[location] = true;
		}
		for(it = head[location].begin();it != head[location].end(); it++)
		{
			data = *it;
			if(visited[data.first] == false)
			{
				stk.push(data.first);
			}
		}
	}
	cout<<endl;
}



void ugraph::bfs(int location)
{
	unvisit();
	queue<int> q;
	q.push(location);
	pair<int, int> data;

	while(!q.empty())
	{
		location = q.front();
		q.pop()
		if(visited[location] == false)
		{
			cout<<location<<" ";
			visited[location] = true;
		}
		for(it=head[location].begin();it != head[location].end();it++)
		{
			data = *it;
			if(visited[data.first] == false)
			{
				q.push(data.first);
			}
		}
	}
	cout<<endl;
}


int main(void)
{
	ugraph g(4);
	g.add_edge(0,2,1);
	g.add_edge(3,2);
	g.add_edge(2,1);

	g.show();
	g.dfs(2);
	g.bfs(2);
	return 0;
}










