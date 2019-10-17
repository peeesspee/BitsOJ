#include<bits/stdc++.h>
using namespace std;

class ugraph{
    private:
        int node_count = 0;
        vector<int> *head;
        vector<int> :: iterator it;
        bool *visited;
        void unvisit(){
            for(int i=0;i<node_count;i++)
            {
                visited[i] = false;
            }
        }
    public:
        ugraph(int nodes)
        {
            node_count = 0;
            head = new vector<int>[nodes];
            visited = new bool[nodes];
        }
        void add_node(int);
        void add_edge(int,int);
        void show();
        void dfs();
        void bfs();
};


void ugraph::add_node(int node_value)
{
    head[node_count].push_back(node_value);
    node_count++;
    return;
}


void ugraph::add_edge(int first_node,int second_node)
{
    head[first_node].push_back(second_node);
    head[second_node].push_back(first_node);
    return;
}


void ugraph::show()
{
    cout<<"Graph\n";
    cout<<"Node - Value : Connections\n";
    for(int i=0;i<node_count;i++)
    {
        cout<<" "<<i<<"-";
        it = head[i].begin();
        cout<<" "<<*it<<" :: ";
        for(it=head[i].begin()+1;it<head[i].end();it++)
        {
            cout<<*it<<"->";
        }
        endl;
    }
}


void ugraph::dfs(int location)
{
    unvisit();
    stack<int> stk;
    stk.push(location);

    while(!stk.empty())
    {
        location = stk.top();
        stk.pop();

        if(visited[location]==false)
        {
            cout<<location<<" ";
            visited[location] = True;
        }
        for(it = head[location].begin() + 1;it = head[location].end();it++)
        {
            if(visited[*it] == false)
            {
                stk.push(*it);
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

    while(!q.empty())
    {
        location = q.front();
        q.pop();
        if(visited[location] == false)
        {
            cout<<location<<" ";
            visited[location] = true;
        }
        for(it = head[location].begin() + 1;it != head[location].end() ; it++)
        {
            if(visited[*it] == false)
            {
                q.push(*it);
            }
        }
    }
    cout<<endl;
}


int main(void)
{
    ugraph g(4);
    g.add_node(4);
    g.add_node(1);
    g.add_node(8);
    g.add_node(5);
    g.add_edge(0,2);
    g.add_edge(3,2);
    g.add_edge(1,2);
    g.show();
    g.dfs();
    g.bfs();
    return 0;
}











