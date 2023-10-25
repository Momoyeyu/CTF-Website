import axios from 'axios';

const BASE_URL = 'http://your-api-base-url.com'; // 替换为实际的API基础URL

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
});

export const createTeam = async (leaderId, teamName, allowJoin) => {
    try {
      const response = await api.post('/api/common/team?action=create_team', {
        action: 'create_team',
        data: {
          leader_id: leaderId,
          team_name: teamName,
          allow_join: allowJoin,
        },
      });
      return response.data;
    } catch (error) {
      throw error;
    }
};
  

export const deleteTeam = async (leaderId, teamName) => {
    try {
      const response = await api.post('/api/common/team?action=del_team', {
        action: 'del_team',
        data: {
          leader_id: leaderId,
          team_name: teamName,
        },
      });
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