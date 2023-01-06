#include <bits/stdc++.h>
using namespace std;

bool issafe(vector<string>&grid,vector<vector<bool>>& vis,int i,int j){
    if(i<0 || i>=grid.size()||j<0||j>=grid[0].size()||vis[i][j]||grid[i][j]=='#'){
        return false;
    }
    return true;
}
void helper(vector<string>&grid){
    int si=-1,sj=-1,ei=-1,ej=-1;
    for(int i=0;i<grid.size();i++){
        for(int j=0;j<grid[i].size();j++){
            if(grid[i][j]=='S'){
                si=i;
                sj=j;
            }
            if(grid[i][j]=='E'){
                ei=i;
                ej=j;
            }
        }
    }
    queue<pair<int,int>>q;
    vector<vector<bool>> vis(grid.size(),vector<bool>(grid[0].size(),false));
    vector<vector<pair<int,int>>> paths;
    q.push({si,sj});
    bool flag=false;
    while(!q.empty()){
        int size=q.size();
        vector<pair<int,int>> p;
        for(int i=0;i<size;i++){
          pair<int,int> temp=q.front();
          q.pop();
        //   cout<<temp.first<<" "<<temp.second<<endl;
          vis[temp.first][temp.second]=true;
          p.push_back({temp.first,temp.second});
          if(grid[temp.first][temp.second]=='E'){
              flag=true;
              break;
          }
          if(issafe(grid,vis,temp.first+1,temp.second)){
             q.push({temp.first+1,temp.second});
          }
          if(issafe(grid,vis,temp.first,temp.second+1)){
             q.push({temp.first,temp.second+1});
          }
          if(issafe(grid,vis,temp.first-1,temp.second)){
             q.push({temp.first-1,temp.second});
          }
          if(issafe(grid,vis,temp.first,temp.second-1)){
             q.push({temp.first,temp.second-1});
          }
        }
        paths.push_back(p);
        if(flag){
            break;
        }
        
    }
    vector<pair<int,int>> ans;
    if(!flag){
        cout<<"Trapped"<<endl;
    }else{
        int pi=ei,pj=ej;
        for(int i=paths.size()-2;i>=1;i--){
            for(int j=0;j<paths[i].size();j++){
               if(paths[i][j].first==pi+1 && paths[i][j].second==pj){
                   ans.push_back(paths[i][j]);
                   pi=paths[i][j].first;
                   pj= paths[i][j].second;
               }else if(paths[i][j].first==pi-1 && paths[i][j].second==pj){
                   ans.push_back(paths[i][j]);
                   pi=paths[i][j].first;
                   pj= paths[i][j].second;
               }else if(paths[i][j].first==pi && paths[i][j].second==pj+1){
                   ans.push_back(paths[i][j]);
                   pi=paths[i][j].first;
                   pj= paths[i][j].second;
               }else if(paths[i][j].first==pi && paths[i][j].second==pj-1){
                   ans.push_back(paths[i][j]);
                   pi=paths[i][j].first;
                   pj= paths[i][j].second;
               }
               
            }

        }
        for(int i=0;i<ans.size();i++){
            grid[ans[i].first][ans[i].second]='*';
        }
        for(int i=0;i<grid.size();i++){
            for(int j=0;j<grid[i].size();j++){
                cout<<grid[i][j];
            }
            cout<<endl;
        }
    }
    
}
int main()
{
    string line;
    vector<string> grid;
    int n;
    cin>>n;
    while(n--){
      cin>>line;
      grid.push_back(line);
    }
    helper(grid);
    return 0;
}
