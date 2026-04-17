#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
华语音乐榜工具 - 高互动版点评文案
包含：情绪共鸣、场景推荐、冷知识、互动引导
"""

import requests
import json
import os
import random
from datetime import datetime
from typing import List, Dict
from collections import OrderedDict


class MusicReviewGenerator:
    """高互动版音乐点评生成器"""
    
    def __init__(self):
        # 歌曲详细数据库（扩充版）
        self.song_database = {
            '跳楼机': {
                'singer': 'LBI利比',
                'style': '电子流行',
                'play_count': '2.3亿',
                'collect_count': '530万',
                'chart_weeks': '12周',
                'peak_rank': 1,
                'first_chart_date': '2026-01-15',
                'highlight': '副歌的电子音色营造出坠落感，像坐过山车一样刺激',
                'feeling': '上头程度：⭐⭐⭐⭐⭐ | 听完想蹦迪',
                'scene': '夜跑、健身、深夜emo',
                'fun_fact': '抖音话题播放超150亿次，2025年现象级爆款',
                'emotion': '释放压力｜刺激过瘾',
                'tags': ['上头', '电子', '氛围感', '神曲']
            },
            '一点': {
                'singer': 'Pezzi / Muyoi',
                'style': '流行说唱',
                'play_count': '8900万',
                'collect_count': '120万',
                'chart_weeks': '8周',
                'peak_rank': 2,
                'first_chart_date': '2026-02-01',
                'highlight': '两人声线互补，hook旋律让人忍不住跟着哼',
                'feeling': '青春感：⭐⭐⭐⭐⭐ | 听完想谈恋爱',
                'scene': '开车、约会、下午茶',
                'fun_fact': '两位00后新人的合作曲，上线一周破千万播放',
                'emotion': '甜蜜｜青春｜治愈',
                'tags': ['青春', '说唱', '治愈', '甜蜜']
            },
            '小美满': {
                'singer': '周深',
                'style': '影视OST',
                'play_count': '5.6亿',
                'collect_count': '890万',
                'chart_weeks': '26周',
                'peak_rank': 1,
                'first_chart_date': '2024-07-20',
                'highlight': '周深空灵嗓音唱出生活的小确幸',
                'feeling': '治愈指数：⭐⭐⭐⭐⭐ | 听完想给生活比个耶',
                'scene': '起床闹钟、工作背景音、睡前',
                'fun_fact': '《热辣滚烫》OST，贾玲说这是她最爱的一首',
                'emotion': '温暖｜治愈｜希望',
                'tags': ['治愈', '温暖', '影视金曲', '周深']
            },
            '纯妹妹': {
                'singer': '单依纯',
                'style': 'R&B',
                'play_count': '2.1亿',
                'collect_count': '310万',
                'chart_weeks': '18周',
                'peak_rank': 2,
                'first_chart_date': '2025-10-10',
                'highlight': '转音丝滑到起鸡皮疙瘩，新生代唱功天花板',
                'feeling': '丝滑程度：⭐⭐⭐⭐⭐ | 单曲循环预定',
                'scene': '咖啡店、发呆、深夜',
                'fun_fact': '单依纯自己写的第一首R&B，上线即登顶各大榜单',
                'emotion': '慵懒｜高级｜治愈',
                'tags': ['R&B', '新生代', '丝滑', '单依纯']
            },
            '向云端': {
                'singer': '小霞/海洋Bo',
                'style': '民谣说唱',
                'play_count': '3.8亿',
                'collect_count': '450万',
                'chart_weeks': '22周',
                'peak_rank': 1,
                'first_chart_date': '2025-08-05',
                'highlight': '副歌空灵治愈，rap部分走心扎心',
                'feeling': '治愈指数：⭐⭐⭐⭐⭐ | 听完想去旅行',
                'scene': '旅行、放松、冥想',
                'fun_fact': '被网友称为"2025年最佳治愈神曲"',
                'emotion': '治愈｜自由｜向往',
                'tags': ['民谣', '治愈', '走心', '旅行']
            },
            '花开忘忧': {
                'singer': '周深',
                'style': '抒情流行',
                'play_count': '8.2亿',
                'collect_count': '1200万',
                'chart_weeks': '163周',
                'peak_rank': 1,
                'first_chart_date': '2023-05-15',
                'highlight': '歌词诗意，情感层层递进，听哭无数人',
                'feeling': '催泪指数：⭐⭐⭐⭐⭐ | 听完想起很多往事',
                'scene': '深夜独处、想念某人',
                'fun_fact': '腾讯音乐榜在榜时间最长歌曲（163周），3年还在榜',
                'emotion': '催泪｜回忆｜思念',
                'tags': ['催泪', '诗意', '经典', '周深']
            },
            '乌梅子酱': {
                'singer': '李荣浩',
                'style': '流行摇滚',
                'play_count': '12.5亿',
                'collect_count': '2100万',
                'chart_weeks': '45周',
                'peak_rank': 1,
                'first_chart_date': '2024-12-01',
                'highlight': '吉他riff抓耳，歌词甜而不腻',
                'feeling': '甜度：⭐⭐⭐⭐⭐ | 像初恋的味道',
                'scene': '约会、表白、婚礼',
                'fun_fact': '李荣浩为杨丞琳写的歌，网友：这就是爱情的样子',
                'emotion': '甜蜜｜上头｜浪漫',
                'tags': ['甜蜜', '上头', '流行', '李荣浩']
            },
            '我记得': {
                'singer': '赵雷',
                'style': '民谣',
                'play_count': '4.2亿',
                'collect_count': '680万',
                'chart_weeks': '35周',
                'peak_rank': 3,
                'first_chart_date': '2024-08-10',
                'highlight': '赵雷式叙事，歌词像电影一样',
                'feeling': '走心指数：⭐⭐⭐⭐⭐ | 听完想给妈妈打电话',
                'scene': '深夜、独处、思念家人',
                'fun_fact': '赵雷时隔6年的催泪之作，网易云评论破50万',
                'emotion': '思念｜亲情｜治愈',
                'tags': ['民谣', '走心', '赵雷', '催泪']
            },
            '孤勇者': {
                'singer': '陈奕迅',
                'style': '流行摇滚',
                'play_count': '28亿',
                'collect_count': '3500万',
                'chart_weeks': '120周',
                'peak_rank': 1,
                'first_chart_date': '2021-11-08',
                'highlight': '陈奕迅教科书级演唱，每句都是金句',
                'feeling': '燃度：⭐⭐⭐⭐⭐ | 听完想去战斗',
                'scene': '健身、打游戏、低谷期',
                'fun_fact': '《英雄联盟》双城之战主题曲，小学生都会唱',
                'emotion': '燃｜励志｜热血',
                'tags': ['励志', '燃', '陈奕迅', 
