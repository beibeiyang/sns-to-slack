/////////////////////////////////////////
// Centralized config file for Lambda
/////////////////////////////////////////

const config = {
  slack: {
    hostname: 'hooks.slack.com',
    port: 443,
    endpoint: "https://hooks.slack.com/services/S0XT0BQ3V609U2NRSAF/wQoAdEcl2jCPpkBd4XAiHzW0",
    channel: "#your_slack_channel",
    username: "AWS SNS via Lambda",
    icon_emoji: ":email:"
  }
};

module.exports = config;
