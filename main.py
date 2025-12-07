# 在这个文件里编写代码
import random

def print_intro():
    """打印程序介绍信息"""
    print("乒乓球比赛模拟器")
    print("功能：")
    print("1. 模拟乒乓球单打比赛（七局四胜制）")
    print("2. 计算两个选手的获胜概率")
    print("3. 支持自定义比赛次数")

def game_over(score_a, score_b):
    """判断一局比赛是否结束"""
    if (score_a >= 11 or score_b >= 11) and abs(score_a - score_b) >= 2:
        return True
    elif score_a == 10 and score_b == 10:
        return False  
    else:
        return False

def simulate_game(prob_a, prob_b):
    """模拟一局比赛"""
    score_a = 0
    score_b = 0
    serving = "A" 
    while not game_over(score_a, score_b):
        if serving == "A":
            if random.random() < prob_a:
                score_a += 1
            else:
                score_b += 1
            serving = "B" 
        else:
            if random.random() < prob_b:
                score_b += 1
            else:
                score_a += 1
            serving = "A"
    return score_a, score_b

def simulate_match(prob_a, prob_b, best_of=7):
    """模拟一场比赛（多局）"""
    wins_a = 0
    wins_b = 0
    while wins_a < best_of // 2 + 1 and wins_b < best_of // 2 + 1:
        score_a, score_b = simulate_game(prob_a, prob_b)
        if score_a > score_b:
            wins_a += 1
        else:
            wins_b += 1
    return wins_a > wins_b

def main():
    print_intro()
    try:
        prob_a = float(input("请输入选手A的能力值（0-1）: "))
        prob_b = float(input("请输入选手B的能力值（0-1）: "))
        simulations = int(input("请输入模拟次数: "))

        if not (0 <= prob_a <= 1 and 0 <= prob_b <= 1):
            raise ValueError("能力值必须在0到1之间")
        if simulations <= 0:
            raise ValueError("模拟次数必须大于0")

        wins_a = 0
        for _ in range(simulations):
            if simulate_match(prob_a, prob_b):
                wins_a += 1
        wins_b = simulations - wins_a

        print("\n模拟结果:")
        print(f"选手A获胜次数: {wins_a} ({wins_a / simulations * 100:.1f}%)")
        print(f"选手B获胜次数: {wins_b} ({wins_b / simulations * 100:.1f}%)")
    except ValueError as e:
        print(f"输入错误: {e}")

if __name__ == "__main__":
    main()
