<template>
    <div id="manageTeam">
      <router-link to="/Home" class="close-btn">&#10006;</router-link>
      <h1>战队管理</h1>
      <p>
        战队名称：{{ team.name }}  &nbsp; 战队人数: {{ team.membernum }}/{{ team.maxnum }}
        <button @click="changeteaminfo()">修改名称</button>
      </p>
      <h2>战队成员</h2>
      <div class="scrollable-table-container">
        <table class="three-column-table">
        <thead>
            <tr>
            <th>成员</th>
            <th>积分</th>
            <th>操作</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="member in members" :key="member.id">
            <td>{{ member.name }}</td>
            <td>{{ member.score }}</td>
            <td>
                <button @click="removeMember(member.id)">移出战队</button>
            </td>
            </tr>
        </tbody>
        </table>
      </div>
      <br>
      <h3 v-if="team.check">申请审核</h3>
      <div class="scrollable-table-container">
        <table class="three-column-table" v-if="team.check">
        <thead>
            <tr>
            <th>申请</th>
            <th>积分</th>
            <th>操作</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="applicant in applicants" :key="applicant.id">
            <td>{{ applicant.name }}</td>
            <td>{{ applicant.score }}</td>
            <td>
                <button @click="approveApplicant(applicant.id)">通过</button>
                <button @click="rejectApplicant(applicant.id)">拒绝</button>
            </td>
            </tr>
        </tbody>
        </table>
      </div>
      <br><br>
      <button @click="disbandTeam">解散战队</button>
    </div>
</template>
  
<script>
  export default {
    data() {
      return {
        team: {
            name:'ezctf',
            membernum:'4',
            maxnum:'10',
            check:true
        },
        members: [
          { id: 1, name: "jwf", score: 100 },
          { id: 2, name: "yyl", score: 100 },
          { id: 3, name: "lwk", score: 100 },
          { id: 4, name: "sjj", score: 100 },
        ],
        applicants: [
          { id: 1, name: "张三", score: 59 },
          { id: 2, name: "李四", score: 99 },
        ],
      };
    },
    methods: {
      async deleteTeam() {
        try {
          const response = await deleteTeam(this.team.name);
          console.log('删除队伍响应:', response);
        } catch (error) {
          console.error('错误:', error);
        }
      },
      removeMember(memberId) {
        // 从战队移出成员的逻辑
        console.log(`成员 ${memberId} 已被移出战队`);
      },
      approveMember(memberId) {
        // 审核通过新成员的逻辑
        console.log(`成员 ${memberId} 已被审核通过`);
      },
      rejectMember(memberId) {
        // 拒绝新成员的逻辑
        console.log(`成员 ${memberId} 的申请已被拒绝`);
      },
    },
  };
</script>

<style>
#manageTeam {
    margin-left: 5%;
    position: fixed;
    top: auto;
    left: auto;
    width: 80%;
    background-color: rgba(0, 0, 0, 0.5);
    justify-content: center;
    align-items: center;
    background-color: #0d1117;
    padding: 20px;
    border-style: solid;
    border-radius: 5px;
    border-color:white;
    border-width: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    text-align: center;
    color:white;
    z-index: 2;
}
.close-btn {
    text-decoration: none;
    color:white;
    position: absolute;
    top: 10px;
    right: 10px;
    cursor: pointer;
}
.scrollable-table-container {
  max-height: 160px; 
  overflow-y: auto; 
}
.three-column-table {
  width: 60%;
  margin-left: 20%;
}

.three-column-table th,
.three-column-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: center;
}

.three-column-table th:first-child,
.three-column-table td:first-child {
  text-align: center;
}
</style>
  