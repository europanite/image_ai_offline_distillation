import { useMemo, useState } from 'react';
import { ActivityIndicator, Pressable, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';

const API_BASE = process.env.EXPO_PUBLIC_API_BASE || 'http://localhost:8000';

type Report = Record<string, unknown>;

function compactJson(value: unknown): string {
  return JSON.stringify(value, null, 2);
}

function LayerBox({ label, detail }: { label: string; detail?: string }) {
  return (
    <View style={styles.layerBox}>
      <Text style={styles.layerLabel}>{label}</Text>
      {detail ? <Text style={styles.layerDetail}>{detail}</Text> : null}
    </View>
  );
}

function DownArrow() {
  return <Text style={styles.downArrow}>↓</Text>;
}

function RightArrow() {
  return <Text style={styles.rightArrow}>→</Text>;
}

function NetworkDiagram({ teacher }: { teacher: string }) {
  return (
    <View style={styles.card}>
      <Text style={styles.sectionTitle}>Teacher / Student Network</Text>
      <Text style={styles.hint}>
        The teacher runs once to create cached logits. The student is trained later from the cached logits only.
      </Text>

      <View style={styles.networkDiagram}>
        <View style={[styles.networkColumn, styles.teacherColumn]}>
          <Text style={[styles.networkTitle, styles.teacherTitle]}>Teacher: {teacher || 'resnet18'}</Text>
          <LayerBox label="Input image" detail="224 × 224 × 3" />
          <DownArrow />
          <LayerBox label="Conv + Residual Stages" detail="public ImageNet model" />
          <DownArrow />
          <LayerBox label="Global Avg Pool" />
          <DownArrow />
          <LayerBox label="1000 logits" detail="teacher output" />
        </View>

        <View style={styles.arrowColumn}>
          <RightArrow />
        </View>

        <View style={styles.cacheColumn}>
          <Text style={styles.cacheTitle}>Offline cache</Text>
          <View style={styles.cacheBox}>
            <Text style={styles.cacheFile}>teacher_logits_train.pt</Text>
            <Text style={styles.cacheDetail}>saved teacher logits</Text>
          </View>
          <Text style={styles.cacheNote}>Teacher is NOT called during student training.</Text>
        </View>

        <View style={styles.arrowColumn}>
          <RightArrow />
        </View>

        <View style={[styles.networkColumn, styles.studentColumn]}>
          <Text style={[styles.networkTitle, styles.studentTitle]}>Student: Small CNN</Text>
          <LayerBox label="Conv 16" />
          <DownArrow />
          <LayerBox label="Conv 32" />
          <DownArrow />
          <LayerBox label="Conv 64" />
          <DownArrow />
          <LayerBox label="Avg Pool" />
          <DownArrow />
          <LayerBox label="Linear 1000" detail="student logits" />
        </View>
      </View>

      <View style={styles.metricRow}>
        <View style={styles.metricChip}>
          <Text style={styles.metricLabel}>teacher_student_top1_agreement</Text>
        </View>
        <View style={styles.metricChip}>
          <Text style={styles.metricLabel}>distillation_kl</Text>
        </View>
        <View style={styles.metricChip}>
          <Text style={styles.metricLabel}>student_parameters</Text>
        </View>
      </View>
    </View>
  );
}

export default function HomeScreen() {
  const [teacher, setTeacher] = useState('resnet18');
  const [dataset, setDataset] = useState('fake');
  const [samples, setSamples] = useState('128');
  const [epochs, setEpochs] = useState('2');
  const [temperature, setTemperature] = useState('3.0');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('Ready.');
  const [report, setReport] = useState<Report | null>(null);

  const payload = useMemo(
    () => ({
      teacher,
      dataset,
      samples: Number(samples),
      batch_size: 16,
      epochs: Number(epochs),
      learning_rate: 0.001,
      temperature: Number(temperature),
      device: 'cpu',
    }),
    [teacher, dataset, samples, epochs, temperature],
  );

  async function post(path: string, body: unknown) {
    setLoading(true);
    setStatus(`Running ${path} ...`);
    try {
      const response = await fetch(`${API_BASE}${path}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      const json = await response.json();
      if (!response.ok) {
        throw new Error(json.detail || `HTTP ${response.status}`);
      }
      setReport(json.report || json);
      setStatus(json.message || 'Done.');
    } catch (error) {
      setStatus(error instanceof Error ? error.message : String(error));
    } finally {
      setLoading(false);
    }
  }

  async function loadReport() {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/api/v1/distillation/report`);
      setReport(await response.json());
      setStatus('Loaded report.');
    } catch (error) {
      setStatus(error instanceof Error ? error.message : String(error));
    } finally {
      setLoading(false);
    }
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Image Offline Distillation</Text>
      <Text style={styles.subtitle}>
        Cache logits from a public ImageNet teacher model, then train a small CNN student without calling the teacher again.
      </Text>

      <View style={styles.layout}>
        <View style={styles.leftPane}>
          <View style={styles.card}>
            <Text style={styles.sectionTitle}>Configuration</Text>

            <Text style={styles.label}>Teacher model</Text>
            <TextInput style={styles.input} value={teacher} onChangeText={setTeacher} />
            <Text style={styles.hint}>Examples: resnet18, resnet50, mobilenet_v3_large</Text>

            <Text style={styles.label}>Dataset</Text>
            <TextInput style={styles.input} value={dataset} onChangeText={setDataset} />
            <Text style={styles.hint}>Use fake for a smoke test. Use image_folder for your own images under data/images.</Text>

            <Text style={styles.label}>Samples</Text>
            <TextInput style={styles.input} value={samples} onChangeText={setSamples} keyboardType="numeric" />

            <Text style={styles.label}>Epochs</Text>
            <TextInput style={styles.input} value={epochs} onChangeText={setEpochs} keyboardType="numeric" />

            <Text style={styles.label}>Temperature</Text>
            <TextInput style={styles.input} value={temperature} onChangeText={setTemperature} keyboardType="numeric" />
          </View>

          <View style={styles.buttonRow}>
            <Pressable style={styles.button} onPress={() => post('/api/v1/distillation/cache-teacher', payload)} disabled={loading}>
              <Text style={styles.buttonText}>1. Cache teacher logits</Text>
            </Pressable>
            <Pressable style={styles.button} onPress={() => post('/api/v1/distillation/train-student', payload)} disabled={loading}>
              <Text style={styles.buttonText}>2. Train student</Text>
            </Pressable>
            <Pressable style={styles.primaryButton} onPress={() => post('/api/v1/distillation/run-all', payload)} disabled={loading}>
              <Text style={styles.buttonText}>Run all</Text>
            </Pressable>
            <Pressable style={styles.secondaryButton} onPress={loadReport} disabled={loading}>
              <Text style={styles.secondaryButtonText}>Load report</Text>
            </Pressable>
          </View>
        </View>

        <View style={styles.rightPane}>
          <NetworkDiagram teacher={teacher} />
        </View>
      </View>

      <View style={styles.statusBox}>
        {loading ? <ActivityIndicator /> : null}
        <Text testID="status" style={styles.status}>{status}</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.sectionTitle}>Report</Text>
        <Text testID="report" style={styles.mono}>{report ? compactJson(report) : 'No report yet.'}</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 24,
    gap: 16,
    backgroundColor: '#f7f7f7',
    minHeight: '100%',
  },
  title: { fontSize: 28, fontWeight: '700' },
  subtitle: { fontSize: 16, lineHeight: 24, color: '#444' },
  layout: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 16,
    alignItems: 'flex-start',
  },
  leftPane: {
    flexGrow: 1,
    flexShrink: 1,
    flexBasis: 340,
    gap: 16,
  },
  rightPane: {
    flexGrow: 2,
    flexShrink: 1,
    flexBasis: 620,
  },
  card: {
    backgroundColor: 'white',
    borderRadius: 16,
    padding: 16,
    gap: 8,
    borderWidth: 1,
    borderColor: '#e5e5e5',
  },
  label: { fontWeight: '700', marginTop: 8 },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 10,
    padding: 10,
    backgroundColor: 'white',
  },
  hint: { color: '#666', fontSize: 12, lineHeight: 18 },
  buttonRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 10 },
  button: { backgroundColor: '#333', padding: 12, borderRadius: 10 },
  primaryButton: { backgroundColor: '#0f766e', padding: 12, borderRadius: 10 },
  secondaryButton: { backgroundColor: 'white', padding: 12, borderRadius: 10, borderWidth: 1, borderColor: '#999' },
  buttonText: { color: 'white', fontWeight: '700' },
  secondaryButtonText: { color: '#333', fontWeight: '700' },
  statusBox: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  status: { fontSize: 14, color: '#333' },
  sectionTitle: { fontSize: 18, fontWeight: '700' },
  mono: { fontFamily: 'monospace', fontSize: 12 },
  networkDiagram: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 10,
    alignItems: 'center',
    marginTop: 8,
  },
  networkColumn: {
    minWidth: 180,
    flexGrow: 1,
    flexShrink: 1,
    borderRadius: 14,
    borderWidth: 1,
    padding: 12,
    gap: 6,
  },
  teacherColumn: {
    backgroundColor: '#eff6ff',
    borderColor: '#93c5fd',
  },
  studentColumn: {
    backgroundColor: '#ecfdf5',
    borderColor: '#86efac',
  },
  networkTitle: {
    fontWeight: '800',
    marginBottom: 4,
  },
  teacherTitle: { color: '#1d4ed8' },
  studentTitle: { color: '#047857' },
  layerBox: {
    backgroundColor: 'white',
    borderColor: '#d4d4d4',
    borderWidth: 1,
    borderRadius: 10,
    padding: 10,
  },
  layerLabel: { fontWeight: '700', color: '#222' },
  layerDetail: { color: '#666', fontSize: 12, marginTop: 2 },
  downArrow: {
    textAlign: 'center',
    fontSize: 18,
    color: '#555',
    fontWeight: '700',
  },
  arrowColumn: {
    minWidth: 28,
    alignItems: 'center',
  },
  rightArrow: {
    fontSize: 28,
    color: '#555',
    fontWeight: '800',
  },
  cacheColumn: {
    minWidth: 190,
    flexGrow: 1,
    flexShrink: 1,
    alignItems: 'stretch',
    gap: 8,
  },
  cacheTitle: {
    fontWeight: '800',
    color: '#7c3aed',
  },
  cacheBox: {
    borderRadius: 14,
    borderWidth: 1,
    borderStyle: 'dashed',
    borderColor: '#a78bfa',
    backgroundColor: '#f5f3ff',
    padding: 14,
  },
  cacheFile: {
    fontFamily: 'monospace',
    fontWeight: '800',
    color: '#4c1d95',
  },
  cacheDetail: {
    color: '#6d28d9',
    marginTop: 4,
    fontSize: 12,
  },
  cacheNote: {
    color: '#92400e',
    backgroundColor: '#fffbeb',
    borderColor: '#fbbf24',
    borderWidth: 1,
    borderRadius: 10,
    padding: 10,
    fontWeight: '700',
  },
  metricRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
    marginTop: 12,
  },
  metricChip: {
    backgroundColor: '#f3f4f6',
    borderColor: '#d1d5db',
    borderWidth: 1,
    borderRadius: 999,
    paddingVertical: 6,
    paddingHorizontal: 10,
  },
  metricLabel: {
    fontSize: 12,
    color: '#374151',
    fontFamily: 'monospace',
  },
});
