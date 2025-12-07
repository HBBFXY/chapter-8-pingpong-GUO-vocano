import random
import matplotlib.pyplot as plt

# 设置中文字体（避免图表中文乱码）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class TableTennisMatch:
    """乒乓球比赛模拟类"""
    def __init__(self, p1_win_prob, best_of=5):
        """
        初始化比赛参数
        :param p1_win_prob: 选手1每球获胜的概率（0-1）
        :param best_of: 比赛局数（5局3胜/7局4胜，默认5局3胜）
        """
        self.p1_prob = p1_win_prob  # 选手1每球胜率
        self.p2_prob = 1 - p1_win_prob  # 选手2每球胜率
        self.best_of = best_of  # 总局数（5/7）
        self.win_needed = (best_of // 2) + 1  # 获胜需要的局数
        self.match_results = []  # 存储多轮模拟的比赛结果
        self.round_scores = []   # 存储每轮比赛的局分详情

    def simulate_game(self):
        """模拟单局比赛，返回局获胜方（1/2）和该局双方得分"""
        p1_score, p2_score = 0, 0
        while True:
            # 随机决定当前球获胜方
            if random.random() < self.p1_prob:
                p1_score += 1
            else:
                p2_score += 1

            # 判定局胜负（11分制，领先2分获胜；10平后需领先2分）
            if (p1_score >= 11 or p2_score >= 11) and abs(p1_score - p2_score) >= 2:
                winner = 1 if p1_score > p2_score else 2
                return winner, (p1_score, p2_score)

    def simulate_match(self):
        """模拟一场完整比赛，返回比赛获胜方和局分详情"""
        p1_games, p2_games = 0, 0
        game_details = []  # 存储每局的得分：[(p1, p2), ...]
        
        # 模拟局数直到一方达到获胜局数
        while p1_games < self.win_needed and p2_games < self.win_needed:
            game_winner, game_score = self.simulate_game()
            game_details.append(game_score)
            if game_winner == 1:
                p1_games += 1
            else:
                p2_games += 1
        
        match_winner = 1 if p1_games > p2_games else 2
        self.match_results.append(match_winner)
        self.round_scores.append(game_details)
        return match_winner, game_details

    def run_simulation(self, n_times):
        """运行n次比赛模拟，统计结果"""
        self.match_results = []
        self.round_scores = []
        for _ in range(n_times):
            self.simulate_match()
        
        # 统计胜负概率
        p1_win_count = self.match_results.count(1)
        p2_win_count = n_times - p1_win_count
        p1_win_rate = p1_win_count / n_times
        p2_win_rate = p2_win_count / n_times

        # 输出基础统计结果
        print(f"===== 模拟{n_times}场比赛结果 =====")
        print(f"选手1获胜次数：{p1_win_count}，胜率：{p1_win_rate:.2%}")
        print(f"选手2获胜次数：{p2_win_count}，胜率：{p2_win_rate:.2%}")

        # 统计单局得分分布（取所有局的得分）
        all_p1_scores = []
        all_p2_scores = []
        for game_list in self.round_scores:
            for p1, p2 in game_list:
                all_p1_scores.append(p1)
                all_p2_scores.append(p2)
        
        # 绘制得分分布直方图
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        plt.hist(all_p1_scores, bins=range(0, max(all_p1_scores)+2), alpha=0.7, label='选手1')
        plt.xlabel('单局得分')
        plt.ylabel('局数')
        plt.title('选手1单局得分分布')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.hist(all_p2_scores, bins=range(0, max(all_p2_scores)+2), alpha=0.7, label='选手2', color='orange')
        plt.xlabel('单局得分')
        plt.ylabel('局数')
        plt.title('选手2单局得分分布')
        plt.legend()
        plt.tight_layout()
        plt.show()

        return {
            "p1_win_rate": p1_win_rate,
            "p2_win_rate": p2_win_rate,
            "all_game_scores": self.round_scores
        }

# ------------------- 示例：运行模拟 -------------------
if __name__ == "__main__":
    # 初始化：选手1每球胜率55%，5局3胜制
    match_sim = TableTennisMatch(p1_win_prob=0.55, best_of=5)
    # 模拟10000场比赛
    results = match_sim.run_simulation(n_times=10000)# 在这个文件里编写代码
