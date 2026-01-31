export interface StrategyReel {
  day: string;
  topic: string;
  hook_angle: string;
  format: string;
}

export interface WeeklyStrategy {
  week: string;
  goals: string[];
  reels: StrategyReel[];
}
