#!/bin/bash
# Запусти это в корне проекта: bash diagnose.sh

echo "====== ДИАГНОСТИКА CPPCHECK RULES ======"
echo ""

echo "=== 1. Версия cppcheck ==="
cppcheck --version
echo ""

echo "=== 2. Поддержка --rule (должен найти 'strcpy') ==="
echo 'void f(){ char buf[4]; strcpy(buf, "toolong"); }' > /tmp/t.c
cppcheck --rule="strcpy \(" /tmp/t.c 2>&1
echo "Если выше нет '[rule]' или написано 'not compiled with HAVE_RULES' — rules вообще не работают!"
echo ""

echo "=== 3. Реальный токен-стрим из bad-файлов ==="
for f in dataset/files/*_bad.c; do
    echo "--- $f ---"
    cppcheck --rule=".+" "$f" 2>&1 | grep "found '"
done
echo ""

echo "=== 4. Тест ПРАВИЛЬНОГО XML формата (вложенный <message>) ==="
cat > /tmp/rule_correct.xml << 'XML'
<?xml version="1.0"?>
<rule version="1">
  <pattern>strcpy \(</pattern>
  <message>
    <id>cwe_787</id>
    <severity>warning</severity>
    <summary>strcpy found - buffer overflow risk</summary>
  </message>
</rule>
XML
echo "XML:"
cat /tmp/rule_correct.xml
echo ""
echo "Результат:"
cppcheck --rule-file=/tmp/rule_correct.xml dataset/files/cwe787_bad.c 2>&1
echo ""

echo "=== 5. Тест НЕПРАВИЛЬНОГО XML формата (как генерирует LLM) ==="
cat > /tmp/rule_wrong.xml << 'XML'
<rule>
  <pattern>strcpy \(</pattern>
  <message>strcpy found - buffer overflow risk</message>
  <severity>warning</severity>
  <id>cwe_787</id>
</rule>
XML
echo "XML:"
cat /tmp/rule_wrong.xml
echo ""
echo "Результат:"
cppcheck --rule-file=/tmp/rule_wrong.xml dataset/files/cwe787_bad.c 2>&1
echo ""

echo "=== 6. Содержимое сгенерированных правил из results/ ==="
for f in results/rules/*.xml; do
    echo "--- $f ---"
    cat "$f"
    echo ""
done

echo "====== ГОТОВО ======"
