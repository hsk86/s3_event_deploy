import json
from pygments import highlight, lexers, formatters

class S3EventConfig:
    def __init__(self, config_params):
        self.params = config_params

    def __str__(self, pretty=True):
        json_txt = json.dumps((self.Config), indent = 4)
        if pretty is True:
            json_txt = highlight(
                json_txt,
                lexers.JsonLexer(),
                formatters.TerminalFormatter()
            )
        return(json_txt)

    def arn_type(self):
        pass

    def config_type(self):
        pass

    def construct_config(self):
        config = {}
        config['Id'] = self.params['id']
        config[self.arn_type()] = self.params['dest_arn']
        config['Events'] = [self.params['events']]

        filter_rules = []
        if self.params['filter_prefix'] is not None:
            filter_rules.append(
                {
                    'Name': 'prefix',
                    'Value': self.params['filter_prefix']
                }
            )
        if self.params['filter_suffix'] is not None:
            filter_rules.append(
                {
                    'Name': 'suffix',
                    'Value': self.params['filter_suffix']
                }
            )
        if filter_rules != []:
            config['Filter'] = {'Key': {'FilterRules': filter_rules}}

        self.new_config = config
        return(self)

    def update_config(self):
        pass

    def attach_config(self, notif_config):
        if self.config_type() not in notif_config:
            notif_config[self.config_type()] = []
        notif_config[self.config_type()].append(self.new_config)
        return(notif_config)

class TopicConfig(S3EventConfig):
    def __init__(self, config_params):
        S3EventConfig.__init__(self, config_params)

    def arn_type(self):
        return("TopicArn")

    def config_type(self):
        return("TopicConfigurations")

class QueueConfig(S3EventConfig):
    def __init__(self, config_params):
        S3EventConfig.__init__(self, config_params)

    def arn_type(self):
        return("QueueArn")

    def config_type(self):
        return("QueueConfigurations")

class LambdaConfig(S3EventConfig):
    def __init__(self, config_params):
        S3EventConfig.__init__(self, config_params)

    def arn_type(self):
        return("LambdaFunctionArn")

    def config_type(self):
        return("LambdaFunctionConfigurations")