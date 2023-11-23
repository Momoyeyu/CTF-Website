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

export const quitTeam = async () => {
  try {
    const requestData = {
      action: 'quit_team',
    };
    const response = await api.get(`/api/common/team?action=quit_team`, requestData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const searchTeam = async (key_word) => {
  try {
    const response = await api.get(`/api/common/team?action=search_team&keyword=${key_word}`);
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

export const teamDetail = async (teamname) => {
  try {
    const response = await api.get(`/api/common/team?action=team_detail&team_name=${teamname}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const accept = async (name,teamname) => {
  try {
    const requestData = {
      action: 'accept',
      data: {
        inviter: name,
        team_name: teamname,
        accept: true,
      },
    };

    const response = await api.put('/api/common/team?action=accept', requestData);
    return response.data;
  } catch (error) {
    throw error;
  }
};