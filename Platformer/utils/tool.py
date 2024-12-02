import json

ground = [{"x": x, "y": 18} for x in range(501)]

# 5개씩 줄바꿈하여 형식 맞춰 출력하기
formatted_output = '"ground": [\n'
for i in range(0, len(ground), 5):
    formatted_output += "    " + ", ".join(json.dumps(item) for item in ground[i:i+5]) + ",\n"
formatted_output = formatted_output.rstrip(",\n") + "\n]"

# 결과 출력
print(formatted_output)
