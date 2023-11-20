<template>
  <div id="bkg">
    <DeleteTeam v-if="deleteTeam"/>
    <ChangeTeamname v-if="changeTeamname"/>
    <ChangeLeader v-if="changeLeader"/>
    <KickMember v-if="kickMember"/>
    <div id="manageTeam" v-if="manageTeam">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1>战队管理</h1>
      <p>
        战队名称：{{ teamInfo.name }}  &nbsp; 战队人数: {{ teamInfo.membernum }}/{{ teamInfo.maxnum }}
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
                <button @click="changeTeamLeader(member.name)">队长转让</button> |
                <button @click="kickmember(member.name)">移出战队</button>
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
                <button @click="approveApplicant(applicant.id)">通过</button> |
                <button @click="rejectApplicant(applicant.id)">拒绝</button>
            </td>
            </tr>
        </tbody>
        </table>
      </div>
      <br><br>
      <button @click="delete_Team()">解散战队</button>
    </div>
  </div>
</template>
  
<script>
  import DeleteTeam from '@/components/DeleteTeam.vue'
  import ChangeTeamname from '@/components/ChangeTeamname.vue'
  import ChangeLeader from '@/components/ChangeLeader.vue'
  import KickMember from '@/components/KickMember.vue'
  import { mapState, mapMutations } from 'vuex';
  import { changeTeamname } from '@/UserSystemApi/TeamApi';
  export default {
    components:{DeleteTeam,ChangeTeamname,ChangeLeader,KickMember},
    data() {
      return {
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
        team: {},
      };
    },
    computed: {
    ...mapState(['userInfoButtonEnabled','username','teamname','isLeader','isMember','deleteTeam','changeTeamname','manageTeam','newLeader','changeLeader','kickMember','kMember']),
    teamInfo() {
      return{
          leader_name: this.$store.state.username,
          name: this.$store.state.teamname,
          membernum: '4',
          maxnum: '10',
          check: true
      }
    },
    },
    methods: {
      ...mapMutations(['setUserInfoButtonEnabled','setUsername','setTeamname','setIsLeader','setIsMember','setDeleteTeam','setChangeTeamname','setManageTeam','setNewLeader','setChangeLeader','setKMember','setKickMember']),
      close() {
        this.setUserInfoButtonEnabled(true);
        this.$router.push('/');
      },
      delete_Team(){
        this.setDeleteTeam(true);
        this.setManageTeam(false);
      },
      changeTeamLeader(name){
        this.setChangeLeader(true);
        this.setManageTeam(false);
        this.setNewLeader(name);
      },
      changeteaminfo(){
        this.setChangeTeamname(true);
        this.setManageTeam(false);
      },
      kickmember(name) {
        this.setKickMember(true);
        this.setManageTeam(false);
        this.setKMember(name);
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
#bkg{
height:87vh;
background-image:url("../assets/背景.png");
background-size:cover;
}
#manageTeam {
    margin-top: 100px;
    margin-left: 300px;
    position: absolute;
    top: auto;
    left: auto;
    width: 800px;
    justify-content: center;
    align-items: center;
    background-color: #1e1e1e;
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
  