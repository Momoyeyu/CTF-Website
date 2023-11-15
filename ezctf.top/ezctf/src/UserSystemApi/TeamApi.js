import axios from 'axios';
axios.defaults.withCredentials = true;
const BASE_URL = 'http://localhost:80'; 

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const createTeam = async (leaderId, teamName, allowJoin) => {
    try {
      const requestData = {
        action: 'create_team',
        data: {
          leader_id: leaderId,
          team_name: teamName,
          allow_join: allowJoin,
        },
      };
      const response = await api.post('/api/common/team?action=create_team',requestData); 
      return response.data;
    } catch (error) {
      throw error;
    }
};
  
  
export const joinTeam = async (username, teamname) => {
  try {
    const requestData = {
      action: 'join_team',
      data: {
        username: username,
        team_name: teamname,
      },
    };

    const response = await api.put('/api/common/team?action=join_team', requestData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const searchTeam = async (keyword) => {
    try {
      const response = await api.get('/api/common/team?action=search_team', {
        params: {
          action: 'search_team',
          keyword: keyword,
        },
      });
      return response.data;
    } catch (error) {
      throw error;
    }
};

export const changeTeamLeader = async (username,newLeaderName) => {
  try {
    const requestData = {
      action: 'change_team_leader',
      data: {
          username: username,
          new_leader_name: newLeaderName
      },
    };

    const response = await api.put('/api/common/team?action=change_team_leader', requestData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const delete_Team = async (password) => {
  try {
    const response = await api.delete('/api/common/team?action=del_team', {
      action: 'del_team',
      data: {
        password: password
      },
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};