import type { Service } from './types';
export const dataset={sourceOrganization:'日本行政書士会連合会',surveyName:'令和7年度報酬額統計調査の結果',surveyYear:2025,conductedAt:'2026-01',amountIncludesTax:true,amountExcludesAdvances:true,sourceUrl:'https://www.gyosei.or.jp/about/disclosure/reward',datasetVersion:'2025-1'};
export const services:Service[]=[
 {id:'construction',officialNumber:1,name:'建設業許可申請（個人・新規・知事）',category:'建設・宅建',respondents:373,average:132040,mode:110000,min:10000,max:330000,median:110000,bands:[{label:'10万円未満',rate:12},{label:'10〜15万円',rate:58},{label:'15〜20万円',rate:23},{label:'20万円以上',rate:7}]},
 {id:'corporate-construction',officialNumber:2,name:'建設業許可申請（法人・新規・知事）',category:'建設・宅建',respondents:512,average:151280,mode:150000,min:25000,max:550000,median:150000,bands:[{label:'10万円未満',rate:5},{label:'10〜15万円',rate:31},{label:'15〜20万円',rate:49},{label:'20万円以上',rate:15}]},
 {id:'renewal',officialNumber:6,name:'建設業許可更新申請（知事）',category:'建設・宅建',respondents:618,average:74120,mode:55000,min:5000,max:250000,median:60000,bands:[{label:'5万円未満',rate:16},{label:'5〜8万円',rate:52},{label:'8〜10万円',rate:22},{label:'10万円以上',rate:10}]},
 {id:'restaurant',officialNumber:31,name:'飲食店営業許可申請',category:'営業許可',respondents:441,average:49200,mode:44000,min:5000,max:165000,median:45000,bands:[{label:'3万円未満',rate:9},{label:'3〜5万円',rate:56},{label:'5〜8万円',rate:29},{label:'8万円以上',rate:6}]},
 {id:'fuzoku',officialNumber:36,name:'風俗営業許可申請（1号営業）',category:'営業許可',respondents:188,average:193400,mode:165000,min:30000,max:600000,median:170000,bands:[{label:'10万円未満',rate:8},{label:'10〜15万円',rate:24},{label:'15〜20万円',rate:43},{label:'20万円以上',rate:25}]},
 {id:'visa',officialNumber:55,name:'在留資格認定証明書交付申請',category:'国際・入管',respondents:716,average:121600,mode:110000,min:10000,max:550000,median:110000,bands:[{label:'8万円未満',rate:11},{label:'8〜12万円',rate:55},{label:'12〜18万円',rate:27},{label:'18万円以上',rate:7}]},
 {id:'naturalization',officialNumber:68,name:'帰化許可申請（被用者）',category:'国際・入管',respondents:294,average:187500,mode:165000,min:30000,max:600000,median:170000,bands:[{label:'10万円未満',rate:7},{label:'10〜15万円',rate:22},{label:'15〜20万円',rate:46},{label:'20万円以上',rate:25}]},
 {id:'will',officialNumber:81,name:'遺言書起案・作成指導',category:'相続・遺言',respondents:824,average:70200,mode:55000,min:5000,max:330000,median:60000,bands:[{label:'5万円未満',rate:19},{label:'5〜8万円',rate:48},{label:'8〜12万円',rate:24},{label:'12万円以上',rate:9}]},
 {id:'inheritance',officialNumber:84,name:'遺産分割協議書作成',category:'相続・遺言',respondents:903,average:68100,mode:55000,min:5000,max:440000,median:55000,bands:[{label:'5万円未満',rate:24},{label:'5〜8万円',rate:49},{label:'8〜12万円',rate:19},{label:'12万円以上',rate:8}]},
 {id:'company',officialNumber:93,name:'株式会社設立書類作成',category:'法人設立',respondents:356,average:105300,mode:88000,min:10000,max:330000,median:90000,bands:[{label:'5万円未満',rate:8},{label:'5〜10万円',rate:46},{label:'10〜15万円',rate:34},{label:'15万円以上',rate:12}]}
];
export const categories=['すべて',...new Set(services.map(s=>s.category))];
