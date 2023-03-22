const getYesterdayDate = (delimeter = '') => {
  let today     = new Date();
  let yesterday = new Date(today.setDate(today.getDate() - 1));

  let fullYear  = yesterday.getFullYear();
  
  let month     = 1 + yesterday.getMonth();
  month         = month >= 10 ? month : '0' + month;

  let day       = yesterday.getDate();
  day           = day >= 10 ? day : '0' + day;

  return fullYear + delimeter + month + delimeter + day;
}

export { getYesterdayDate };