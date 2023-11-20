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
  
  
export const joinTeam = async (teamname) => {
  try {
    const requestData = {
      action: 'join_team',
      data: {
        team_name: teamname,
      },
    };

    const response = await api.put('/api/common/team?action=join_team', requestData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const searchTeam = async (key_word) => {
    try {
      const requestData = {
        action: 'search_team',
        data: {
          keyword: key_word,
        }
      };

      const response = await api.get('/api/common/team?action=search_team', requestData);
      return response.data;
    } catch (error) {
      throw error;
    }
};

export const changeTeamLeader = async (newLeaderName) => {
  try {
    const requestData = {
      action: 'change_team_leader',
      data: {
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
    const response = await api.delete('/api/common/team?action=del_team', {data:{
      action: 'del_team',
      data: {
        password: password
      },
  }});
    return response.status;
  } catch (error) {
    throw error;
  }
};

export const changeTeamName = async (newTeamName) => {
  try {
    const requestData = {
      action: 'change_team_name',
      data: {
          new_team_name: newTeamName
      },
    };

    const response = await api.put('/api/common/team?action=change_team_name', requestData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const kickoutMember = async (username) => {
  try {
    const requestData = {
      action: 'kick_out',
      data: {
          username: username
      },
    };

    const response = await api.post('/api/common/team?action=kick_out', requestData);
    return response.data;
  } catch (error) {
    throw error;
  }
};