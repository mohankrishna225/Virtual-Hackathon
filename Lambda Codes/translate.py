import boto3
translate = boto3.client('translate')



def english(text):
	response = translate.translate_text(Text=text,SourceLanguageCode="auto",TargetLanguageCode="en")
	#print(response)
	print(response["TranslatedText"])
	return (response["TranslatedText"])

def tamil(text):
	response = translate.translate_text(Text=text,SourceLanguageCode="auto",TargetLanguageCode="ta")
	print(response["TranslatedText"])
	return (response["TranslatedText"])

def hindi(text):
	response = translate.translate_text(Text=text,SourceLanguageCode="auto",TargetLanguageCode="hi")
	print(response["TranslatedText"])
	return (response["TranslatedText"])


english("आप कैसे हो")
tamil("आप कैसे हो")


hindi("mohanharikrishna")