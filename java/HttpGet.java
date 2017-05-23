package cn.mcwen;


import java.io.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;

public class MultiThreadGet {
    private static boolean flag = true;


    public static double gaussian(double x) {

        return 1.0 / Math.sqrt(2.0 * Math.PI) * Math.exp(-1 * Math.pow(x, 2) / 2.0);

    }

    public static class Worker implements Runnable {

        public void run() {

            while (flag) {
                HttpClient httpClient = new DefaultHttpClient();

                HttpGet httpget = new HttpGet("http://115.25.64.9:88");

                HttpResponse response = null;
                try {
                    response = httpClient.execute(httpget);
                    HttpEntity entity = response.getEntity();
                    InputStream instream = entity.getContent();
                    BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(instream, "UTF-8"));
                    String content = null;
                    while ((content = bufferedReader.readLine()) != null) {
                        System.out.println(content);
                    }
                    bufferedReader.close();
                } catch (ClientProtocolException e2) {
                    // TODO Auto-generated catch block
                    e2.printStackTrace();
                } catch (IOException e2) {
                    // TODO Auto-generated catch block
                    e2.printStackTrace();
                }


            }
        }
    }

    public static void constantsModel(int num, long sleepTime) {
        ExecutorService pool = Executors.newFixedThreadPool(num);
        pool.execute(new Worker());
        try {
            Thread.sleep(sleepTime);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        flag = false;
        pool.shutdownNow();
    }

    public static void linearModel(int num, long sleepTime, int slope) {
        for (int i = 0; i < num; i++) {
            flag = true;
            ExecutorService pool = Executors.newFixedThreadPool(i * slope);
            pool.execute(new Worker());
            try {
                Thread.sleep(sleepTime);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            flag = false;
            pool.shutdownNow();
        }
    }

    public static void gaussianModel(int num, long sleepTime) {
        for (double d = -2; d <= 2; d += 0.4) {
            System.out.println((int)(gaussian(d) * num));
            try {
                Thread.sleep(sleepTime);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        constantsModel(10, 100000);
        linearModel(10,100000,2);
        gaussianModel(40,10000);
    }
}
