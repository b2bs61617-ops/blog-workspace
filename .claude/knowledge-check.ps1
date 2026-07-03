$msg = "今日教えた事やスキル、ルールなどはファイルにちゃんと書いた？書いて無ければ今日の覚えた事は全てファイルに書いてと指示して欲しいワン！わんこそば！"
$obj = @{ systemMessage = $msg }
$obj | ConvertTo-Json -Compress