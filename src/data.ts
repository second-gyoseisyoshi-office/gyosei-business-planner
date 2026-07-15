import rawServices from './services.generated.json';
import type { Service } from './types';

export const dataset = {
  sourceOrganization: '日本行政書士会連合会',
  surveyName: '令和7年度報酬額統計調査の結果',
  surveyYear: 2025,
  conductedAt: '2026-01',
  amountIncludesTax: true,
  amountExcludesAdvances: true,
  sourceUrl: 'https://www.gyosei.or.jp/about/disclosure/reward',
  datasetVersion: '2025-full-1',
  serviceCount: 487,
};

export const services = rawServices as Service[];

const categoryOrder = [
  '建設・宅建',
  '土地・農地',
  '営業許可',
  '運輸・自動車',
  '国際・入管',
  '法人・組合',
  '相続・遺言',
  '契約・民事',
  '知財・著作権',
  '環境・廃棄物',
  '労務・社会保険',
  '補助金・融資',
  'その他・経営支援',
];

export const categories = [
  'すべて',
  '任意業務',
  ...categoryOrder.filter(category => services.some(service => service.category === category)),
];
